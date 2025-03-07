import pygame
import sys, random, time

from src.Beat import RGB_Table, RED, BLACK, GREEN, BLUE, CYAN, YELLOW, MAGENTA, ORANGE, WHITE


class Tetrimion:
    def __init__(self, name:str, color: list[int]):
        self.name = name
        self.color = color
        self.pixmap = None
    
    
class ActiveTetrimon:
    def __init__(self, tetrimion: Tetrimion):
        self.tetrimion = tetrimion
        self.coords = [0, 0]
        self.rotation = 0
        self.pixmap = tetrimion.pixmap[self.rotation]

    def move_side(self, direction: bool):
        # direction is True for move to the left
        # direction is False for move to the right
        if direction:
            offset_y = -1
        else:
            offset_y = 1

        if not check_move_xy_collision(target=self, offset_x=0, offset_y=offset_y):
            self.coords[1] += offset_y
            snd_click.play()

    def rotate(self, cw: bool):
        # cw is True: clock-wise i.e. right turn
        # cw is False: counter-clock-wise i.e. left turn
        if cw:
            next_rotation_lookup = [1, 2, 3, 0]
        else:
            next_rotation_lookup = [3, 0, 1, 2]
        self.pixmap = self.tetrimion.pixmap[next_rotation_lookup[self.rotation]]

        if not check_move_xy_collision(target=self, offset_x=0, offset_y=0):
            self.rotation = next_rotation_lookup[self.rotation]
            self.pixmap = self.tetrimion.pixmap[self.rotation]
            snd_click.play()
        else:
            self.pixmap = self.tetrimion.pixmap[self.rotation]

    def drop_down(self):
        while not check_move_xy_collision(target=self, offset_x=1, offset_y=0):
            self.coords[0] += 1
            buildScreen()
            time.sleep(0.01)
        fixTile()

    def move_down(self):
        if not check_move_xy_collision(target=self, offset_x=1, offset_y=0):
            self.coords[0] += 1
        else:
            fixTile()

# See for rotation: https://tetris.wiki/Category:Rotation_systems
I_TILE = Tetrimion("I", CYAN)
I_TILE.pixmap = [
    [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0]],
    [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0]]]
J_TILE = Tetrimion("J", BLUE)
J_TILE.pixmap = [
    [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 1],
     [0, 1, 0],
     [0, 1, 0]],
    [[0, 0, 0],
     [1, 1, 1],
     [0, 0, 1]],
    [[0, 1, 0],
     [0, 1, 0],
     [1, 1, 0]]]
L_TILE = Tetrimion("L", ORANGE)
L_TILE.pixmap = [
    [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 0],
     [0, 1, 0],
     [0, 1, 1]],
    [[0, 0, 0],
     [1, 1, 1],
     [1, 0, 0]],
    [[1, 1, 0],
     [0, 1, 0],
     [0, 1, 0]]]
O_TILE = Tetrimion("O", YELLOW)
O_TILE.pixmap = [
    [[1, 1],
     [1, 1]],
    [[1, 1],
     [1, 1]],
    [[1, 1],
     [1, 1]],
    [[1, 1],
     [1, 1]]]
S_TILE = Tetrimion("S", GREEN)
S_TILE.pixmap = [
    [[0, 0, 0],
     [0, 1, 1],
     [1, 1, 0]],
    [[0, 1, 0],
     [0, 1, 1],
     [0, 0, 1]],
    [[0, 0, 0],
     [0, 1, 1],
     [1, 1, 0]],
    [[0, 1, 0],
     [0, 1, 1],
     [0, 0, 1]]]
T_TILE = Tetrimion("T", MAGENTA)
T_TILE.pixmap = [
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 0],
     [0, 1, 1],
     [0, 1, 0]],
    [[0, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],
    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0]]]
Z_TILE = Tetrimion("Z", RED)
Z_TILE.pixmap = [
    [[0, 0, 0],
     [1, 1, 0],
     [0, 1, 1]],
    [[0, 0, 1],
     [0, 1, 1],
     [0, 1, 0]],
    [[0, 0, 0],
     [1, 1, 0],
     [0, 1, 1]],
    [[0, 0, 1],
     [0, 1, 1],
     [0, 1, 0]]]


def get_blank_playfield(just_bool:bool = False):
    if just_bool:
        return [[0] * 10 for _ in range(22)]
    else:
        return [[BLACK] * 10 for _ in range(22)]


####Global variables
activeTet : ActiveTetrimon(I_TILE)
level = 1
linescleared = 0
playfield = get_blank_playfield()
keyTimeout = 150
keyTime = 0
moveTimeout = 500
moveTime = 0
Tetris_Points = 0


def fadeInOut(rgb):
    display.brightness = 0.0
    display.fill(rgb)
    display.wait_time = 0.01

    while display.brightness < 1.0:
        display.brightness += 0.01
        display.show()
        display.wait()

    while display.brightness > 0.0:
        display.brightness -= 0.01
        display.show()
        display.wait()

    display.fill(BLACK)
    display.show()
    display.brightness = 1.0


def spawn():
    global activeTet, moveTime
    str_list = [I_TILE, O_TILE, T_TILE, S_TILE, Z_TILE, J_TILE, L_TILE]
    random.shuffle(str_list)

    activeTet = ActiveTetrimon(str_list[0])
    if activeTet.tetrimion.name == "I":
        activeTet.coords = [0, 3]
    elif activeTet.tetrimion.name == "J":
        activeTet.coords = [0, 3]
    elif activeTet.tetrimion.name == "L":
        activeTet.coords = [0, 3]
    elif activeTet.tetrimion.name == "O":
        activeTet.coords = [0, 4]
    elif activeTet.tetrimion.name == "S":
        activeTet.coords = [0, 3]
    elif activeTet.tetrimion.name == "Z":
        activeTet.coords = [0, 3]
    elif activeTet.tetrimion.name == "T":
        activeTet.coords = [0, 3]

    moveTime = pygame.time.get_ticks()

    print(f"spawned {activeTet}")
    if check_move_xy_collision(target=activeTet, offset_x=0, offset_y=0):
        print(f"collision {activeTet}")
        raise Exception("Game over")


def check_temp_vs_fixed(temp_pixels):
    global playfield
    for row in range(len(playfield)):
        for col in range(len(playfield[row])):
            if temp_pixels[row][col]:
                if playfield[row][col] != BLACK:
                    return True
    return False


def check_move_xy_collision(target, offset_x, offset_y):
    temp_pixels = get_blank_playfield(just_bool=True)
    for row in range(len(target.pixmap)):
        for col in range(len(target.pixmap[row])):
            if target.pixmap[row][col]:
                x = target.coords[0] + row + offset_x
                y = target.coords[1] + col + offset_y
                if 0 <= x < len(temp_pixels) and  0 <= y < len(temp_pixels[row]):
                    temp_pixels[x][y] = True
                else:
                    return True
    return check_temp_vs_fixed(temp_pixels)


def setLevelAndSpeed():
    global level, moveTimeout, linescleared
    previous_level = level
    if linescleared <= 0:
        level = 1
    elif 1 <= linescleared <= 90:
        level = 1 + ((linescleared - 1) / 10)
    elif linescleared >= 91:
        level = 10

    if level > previous_level:
        snd_level.play()
    moveTimeout = (11 - level) * 50


def checkFinishedLines():
    global playfield
    lines_finished = []
    for row in range(len(playfield)):
        if all(map(lambda x: x != BLACK, playfield[row])):
            lines_finished.append(row)

    for _ in range(3):
        for i in lines_finished:
            playfield[i] = [WHITE] * len(playfield[i])
        buildScreen()
        time.sleep(0.1)
        for i in lines_finished:
            playfield[i] = [BLACK] * len(playfield[i])
        buildScreen()
        time.sleep(0.1)

    lines_finished.reverse()
    print(lines_finished)
    offset = 0
    for i in lines_finished:
        playfield.pop(i + offset)
        playfield.insert(0, [BLACK] * len(playfield[0]))
        offset += 1
        snd_linekill.play()
        buildScreen()

    return len(lines_finished)


def calculate_points(nof_cleared_lines: int):
    global linescleared, level, Tetris_Points
    if nof_cleared_lines == 1:
        Tetris_Points += 40 * level
    elif nof_cleared_lines == 2:
        Tetris_Points += 100 * level
    elif nof_cleared_lines == 3:
        Tetris_Points += 300 * level
    elif nof_cleared_lines == 4:
        Tetris_Points += 1200 * level

    linescleared += nof_cleared_lines


def fixTile():
    global playfield, activeTet, Tetris_Points, level

    # Add the active tetrimino to the fixed pixels with its color
    for row in range(len(activeTet.pixmap)):
        for col in range(len(activeTet.pixmap[row])):
            if activeTet.pixmap[row][col]:
                x = activeTet.coords[0] + row
                y = activeTet.coords[1] + col
                if 0 <= x < len(playfield) and 0 <= y < len(playfield[0]):
                    playfield[x][y] = activeTet.tetrimion.color

    activeTet = None
    buildScreen()
    snd_tilefix.play()
    nof_cleared_lines = checkFinishedLines()
    calculate_points(nof_cleared_lines)
    Tetris_Points += (21 + (3 * level))
    setLevelAndSpeed()
    print(f"Lines cleared: {linescleared} - Level: {level} - moveTimeout: {moveTimeout} - Tetris Points: {Tetris_Points}")

    spawn()


def getKeypress(joystick):
    pygame.event.pump()
    key_pressed = ""
    if joystick.get_axis(1) <= -0.5:  # D-Pad nach oben
        key_pressed = "UP"
    if joystick.get_axis(1) >= +0.5:  # D-Pad nach unten
        key_pressed = "DOWN"
    if joystick.get_axis(0) >= +0.5:  # D-Pad rechts
        key_pressed = "RIGHT"
    if joystick.get_axis(0) <= -0.5:  # D-Pad nach links
        key_pressed = "LEFT"
    if joystick.get_button(0):  # Button A - right red button - Rotate right
        key_pressed = "A"
    if joystick.get_button(1):  # Button B - left red button - Rotate left
        key_pressed = "B"
    if joystick.get_button(10):
        key_pressed = "SELECT"
    if joystick.get_button(11):
        key_pressed = "START"

    return key_pressed


def keyAction(pressed_key):
    if pressed_key == "UP":
        activeTet.drop_down()
    if pressed_key == "DOWN":
        activeTet.move_down()
    if pressed_key == "LEFT":
        activeTet.move_side(True)
    if pressed_key == "RIGHT":
        activeTet.move_side(False)
    if pressed_key == "A":
        activeTet.rotate(True)
    if pressed_key == "B":
        activeTet.rotate(False)


def buildScreen():
    # Overlay fixed and mobile Pixels
    global playfield, activeTet

    for i in range(display.width):
        display.set_pixel(i, 0, WHITE)
        display.set_pixel(i, display.height - 1, WHITE)
    for i in range(display.height):
        display.set_pixel(0, i, WHITE)
        display.set_pixel(display.width - 1, i, WHITE)

    for row in range(len(playfield)):
        for col in range(len(playfield[row])):
            display.set_pixel(row + 1, col + 1, playfield[row][col])

    if activeTet is not None:
        for row in range(len(activeTet.pixmap)):
            for col in range(len(activeTet.pixmap[row])):
                if activeTet.pixmap[row][col]:
                    x = activeTet.coords[0] + row + 1
                    y = activeTet.coords[1] + col + 1
                    if 0 <= x < display.width and 0 <= y < display.height:
                        display.set_pixel(x, y, activeTet.tetrimion.color)
    display.show()


if __name__ == '__main__':
    display = RGB_Table()

    print("Initialize sound system...", end=""),
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    print("done!")

    print("Loading music...", end=""),
    pygame.mixer.music.load('/home/pi/rgb-led-table/sounds/tetrisaccapella.ogg')
    pygame.mixer.music.set_volume(0.4)
    print("done!")

    print("Loading SFX...", end=""),
    snd_click = pygame.mixer.Sound('/home/pi/rgb-led-table/sounds/click.ogg')
    snd_linekill = pygame.mixer.Sound('/home/pi/rgb-led-table/sounds/linekill.ogg')
    snd_tilefix = pygame.mixer.Sound('/home/pi/rgb-led-table/sounds/tilefix.ogg')
    snd_pause = pygame.mixer.Sound('/home/pi/rgb-led-table/sounds/pause.ogg')
    snd_gameover = pygame.mixer.Sound('/home/pi/rgb-led-table/sounds/gameover.ogg')
    snd_level = pygame.mixer.Sound('/home/pi/rgb-led-table/sounds/level.ogg')
    print("done!")

    pygame.mixer.music.play(-1)

    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("How do you want to play Tetris without a joystick?")
        sys.exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f'Initialized Joystick : {joystick.get_name()}')

    print("Game of Tetris started!")
    fadeInOut([128, 128, 128])

    spawn()
    moveTime = keyTime = pygame.time.get_ticks()

    try:
        while True:
            key_press = getKeypress(joystick)
            if key_press == "START":
                print("Game paused")
                pygame.mixer.music.pause()
                snd_pause.play()
                while joystick.get_button(11):
                    pygame.event.pump()
                    time.sleep(0.1)
                while not joystick.get_button(11):
                    pygame.event.pump()
                    time.sleep(0.1)

                print("Game resumed")
                snd_pause.play()
                time.sleep(1)
                pygame.mixer.music.unpause()

            if pygame.time.get_ticks() > keyTime + keyTimeout:
                keyAction(key_press)
                keyTime = pygame.time.get_ticks()
            if pygame.time.get_ticks() > moveTime + moveTimeout:
                activeTet.move_down()
                moveTime = pygame.time.get_ticks()

            buildScreen()
            time.sleep(0.01)        # Throttle down CPU load...

    except Exception as e:
        print(e)

    pygame.mixer.music.stop()
    snd_gameover.play()
    time.sleep(0.1)
    fadeInOut(RED)
    print(f"Game over! {Tetris_Points} points.")
    print("Tetris ended.")
