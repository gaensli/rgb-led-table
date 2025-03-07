import pygame, pickle
import sys, random, time

from src.Beat import RGB_Table, RED, BLACK, GREEN, BLUE, CYAN, YELLOW, MAGENTA, ORANGE, WHITE


class tiles:
    # See for rotation: https://tetris.wiki/Category:Rotation_systems
    EMPTY_TILE = [
        [[1]],
        [[1]],
        [[1]],
        [[1]],
        BLACK
    ]
    I_TILE = [
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
         [0, 0, 1, 0]],
        CYAN]
    J_TILE = [
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
         [1, 1, 0]],
        BLUE]
    L_TILE = [
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
         [0, 1, 0]],
        ORANGE]
    O_TILE = [
        [[1, 1],
         [1, 1]],
        [[1, 1],
         [1, 1]],
        [[1, 1],
         [1, 1]],
        [[1, 1],
         [1, 1]],
        YELLOW]
    S_TILE = [
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
         [0, 0, 1]],
        GREEN]
    T_TILE = [
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
         [0, 1, 0]],
        MAGENTA]
    Z_TILE = [
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
         [0, 1, 0]],
        RED]



def get_blank_playfield(just_bool:bool = False):
    if just_bool:
        return [[0] * 10 for _ in range(22)]
    else:
        return [[BLACK] * 10 for _ in range(22)]


####Global variables
playerName = "Anon"
hiScores = []
activeTet = tiles.EMPTY_TILE
activeTetCoords = [0, 0]
activeTetRotation = 0
level = 1
linescleared = 0
dropPoints = 0
playfield = get_blank_playfield()
keyPressTimeout = 125
keyPressTime = 0
keyTimeout = 150
keyTime = 0
moveTimeout = 500
moveTime = 0
Tetris_Points = 0
running = False
paused = False


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
    global  activeTet, activeTetRotation, activeTetCoords, dropPoints
    str_list = [tiles.I_TILE, tiles.O_TILE, tiles.T_TILE, tiles.S_TILE, tiles.Z_TILE, tiles.J_TILE, tiles.L_TILE]
    random.shuffle(str_list)

    activeTet = str_list[0]
    activeTetRotation = 0
    dropPoints = 0
    if activeTet == tiles.I_TILE:
        activeTetCoords = [0, 3]
    elif activeTet == tiles.J_TILE:
        activeTetCoords = [0, 3]
    elif activeTet == tiles.L_TILE:
        activeTetCoords = [0, 3]
    elif activeTet == tiles.O_TILE:
        activeTetCoords = [0, 4]
    elif activeTet == tiles.S_TILE:
        activeTetCoords = [0, 3]
    elif activeTet == tiles.Z_TILE:
        activeTetCoords = [0, 3]
    elif activeTet == tiles.T_TILE:
        activeTetCoords = [0, 3]
    if check_move_xy_collision(target=activeTet[activeTetRotation], offset_x=0, offset_y=0):
        game_over()


def check_temp_vs_fixed(temp_pixels):
    global playfield
    for row in range(len(playfield)):
        for col in range(len(playfield[row])):
            if temp_pixels[row][col]:
                if playfield[row][col] != BLACK:
                    return True
    return False


def check_move_xy_collision(target, offset_x, offset_y):
    global activeTetCoords
    temp_pixels = get_blank_playfield(just_bool=True)
    for row in range(len(target)):
        for col in range(len(target[row])):
            if target[row][col]:
                x = activeTetCoords[0] + row + offset_x
                y = activeTetCoords[1] + col + offset_y
                if 0 <= x < len(temp_pixels) and  0 <= y < len(temp_pixels[row]):
                    temp_pixels[x][y] = target[row][col]
    return check_temp_vs_fixed(temp_pixels)


def move_side(direction:str):
    if direction == "left":
        offset_y = -1
    elif direction == "right":
        offset_y = 1
    else:
        raise ValueError("direction not recognized")

    global activeTetCoords, activeTet, activeTetRotation
    if not check_move_xy_collision(target=activeTet[activeTetRotation], offset_x=0, offset_y=offset_y):
        activeTetCoords[1] += offset_y
        snd_click.play()


def game_over():
    global activeTet, activeTetCoords, activeTetRotation, playfield, keyTimeout, keyTime, moveTimeout, moveTime, running, paused, Tetris_Points, level, keyPressTime, keyPressTimeout, linescleared, dropPoints

    print(f"Game over! {Tetris_Points} points.")
    pygame.mixer.music.stop()
    snd_gameover.play()
    time.sleep(3)
    fadeInOut([255, 0, 0])
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # sock.sendto(str(Tetris_Points), ("192.168.0.241", 56565))
    entry = (playerName, Tetris_Points)
    hiScores.append(entry)

    def getKey(item):
        return item[1]

    hiScores.sort(key=getKey, reverse=True)
    pickle.dump(hiScores, open("/home/pi/rgb-led-table/hiscores.zfl", "wb"))

    # reset game for next round
    activeTet = tiles.EMPTY_TILE
    activeTetCoords = [0, 0]
    activeTetRotation = 0
    linescleared = 0
    dropPoints = 0
    level = 1
    playfield = get_blank_playfield()
    keyPressTimeout = 150
    keyPressTime = 0
    keyTimeout = 100
    keyTime = 0
    moveTimeout = 200
    moveTime = 0
    Tetris_Points = 0
    running = False
    paused = False


def get_next_rotation(cw: bool):
    # cw i.e. clock-wise i.e. right turn
    # opposite of cw is ccw i.e. counter-clock-wise i.e. left turn
    if cw:
        next_rotation_lookup = [1, 2, 3, 0]
    else:
        next_rotation_lookup = [3, 0, 1, 2]
    return next_rotation_lookup[activeTetRotation]


def rotate(cw: bool):
    global activeTetRotation
    if not check_move_xy_collision(target=activeTet[get_next_rotation(cw)], offset_x=0, offset_y=0):
        activeTetRotation = get_next_rotation(cw)
    snd_click.play()


def drop_down():
    global activeTetCoords, keyTime, moveTime
    while not check_move_xy_collision(target=activeTet[activeTetRotation], offset_x=1, offset_y=0):
        activeTetCoords[0] += 1
        keyTime = pygame.time.get_ticks()
        moveTime = pygame.time.get_ticks()
        buildScreen()
    fixTile()


def move_down():
    global activeTetCoords, dropPoints
    if check_move_xy_collision(target=activeTet[activeTetRotation], offset_x=1, offset_y=0):
        fixTile()
    else:
        activeTetCoords[0] += 1
        dropPoints += 1


def setLevelAndSpeed(lines):
    global level, moveTimeout, Tetris_Points
    previous_level = level
    if linescleared <= 0:
        level = 1
    elif 1 <= lines <= 90:
        level = 1 + ((lines - 1) / 10)
    elif lines >= 91:
        level = 10

    if level > previous_level:
        snd_level.play()
    moveTimeout = (11 - level) * 50
    print(f"Lines cleared: {lines} - Level: {level} - moveTime: {moveTimeout} - Tetris Points: {Tetris_Points}")


def checkFinishedLines():
    global playfield, Tetris_Points, linescleared, level
    linesFinished = 0
    for row in range(len(playfield)):
        if all(map(lambda x: x != BLACK, playfield[row])):
            linesFinished += 1
            playfield[row] = [BLACK] * 10
            buildScreen()
            # TODO wait a bit time
            for mrow in range(row, 0, -1):
                playfield[mrow] = playfield[mrow - 1]
            snd_linekill.play()
            buildScreen()

    if linesFinished == 1:
        Tetris_Points += 40 * level
    elif linesFinished == 2:
        Tetris_Points += 100 * level
    elif linesFinished == 3:
        Tetris_Points += 300 * level
    elif linesFinished == 4:
        Tetris_Points += 1200 * level

    linescleared += linesFinished
    setLevelAndSpeed(linescleared)


def fixTile():
    global playfield, activeTet, activeTetRotation, activeTetCoords, moveTime, running, dropPoints, Tetris_Points, level

    # Add the active tetrimino to the fixed pixels with its color
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][row])):
            if activeTet[activeTetRotation][row][col]:
                x = activeTetCoords[0] + row
                y = activeTetCoords[1] + col
                if 0 <= x < len(playfield) and 0 <= y < len(playfield[0]):
                    playfield[x][y] = activeTet[4]

    activeTet = tiles.EMPTY_TILE
    checkFinishedLines()
    snd_tilefix.play()
    time.sleep(moveTimeout / 1000.0)
    Tetris_Points += ((21 + (3 * level)) - dropPoints)
    spawn()
    if running:
        buildScreen()
    moveTime = pygame.time.get_ticks()


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
    global paused, keyPressTime

    if pressed_key == "UP":
        drop_down()
    if pressed_key == "DOWN":
        move_down()
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "RIGHT":
        move_side("right")
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "LEFT":
        move_side("left")
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "A":
        rotate(True)
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "B":
        rotate(False)
        keyPressTime = pygame.time.get_ticks()

    if pressed_key == "START":
        print("Game paused")
        paused = True
        pygame.mixer.music.pause()
        snd_pause.play()
    buildScreen()


def buildScreen():
    # Overlay fixed and mobile Pixels
    global running, playfield, activeTet, activeTetRotation, activeTetCoords

    if running:
        for i in range(display.width):
            display.set_pixel(i, 0, WHITE)
            display.set_pixel(i, display.height - 1, WHITE)
        for i in range(display.height):
            display.set_pixel(0, i, WHITE)
            display.set_pixel(display.width - 1, i, WHITE)

        for row in range(len(playfield)):
            for col in range(len(playfield[row])):
                display.set_pixel(row + 1, col + 1, playfield[row][col])

        if activeTet is not tiles.EMPTY_TILE:
            for row in range(len(activeTet[activeTetRotation])):
                for col in range(len(activeTet[activeTetRotation][row])):
                    if activeTet[activeTetRotation][row][col]:
                        x = activeTetCoords[0] + row + 1
                        y = activeTetCoords[1] + col + 1
                        if 0 <= x < display.width and 0 <= y < display.height:
                            display.set_pixel(x, y, activeTet[4])
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

    print("Loading Hiscores...", end=""),
    # hiScores = pickle.load(open("/home/pi/rgb-led-table/hiscores.zfl", "rb"))
    # hiScores.sort(key=getKey, reverse=True)
    print("done!")
    # print("Aktueller Hiscore: " + str(hiScores[0][1]) + " Punkte von " + str(hiScores[0][0]))
    #  if len(sys.argv) > 1:
    #        playerName = sys.argv[1]
    #        print("Hi " + playerName + ", good luck!")

    print("Game of Tetris started!")
    fadeInOut([128, 128, 128])

    running = True
    spawn()
    moveTime = pygame.time.get_ticks()
    keyTime = moveTime
    keyPressTime = moveTime
    key_press = ""

    while running:
        if paused:
            time.sleep(1)
            while paused:
                pygame.event.pump()
                if joystick.get_button(11):
                    print("Game resumed")
                    snd_pause.play()
                    pygame.mixer.music.unpause()
                    time.sleep(1)
                    paused = False

        if running:
            if pygame.time.get_ticks() > keyPressTime + keyPressTimeout:
                key_press = getKeypress(joystick)
            if pygame.time.get_ticks() > keyTime + keyTimeout:
                keyAction(key_press)
                keyTime = pygame.time.get_ticks()
            if pygame.time.get_ticks() > moveTime + moveTimeout:
                move_down()
                moveTime = pygame.time.get_ticks()
        if running:
            buildScreen()
    print("Tetris ended.")
