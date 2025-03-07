import pygame, pickle
import sys, random, time

from src.Beat import RGB_Table, RED, BLACK, WHITE, GREEN, BLUE, CYAN, YELLOW, MAGENTA


class gamecolors:
    BG_COLOR = BLACK


class tiles:
    I_TILE = [[[1, 1, 1, 1]],
              [[1],
               [1],
               [1],
               [1]],
              [[1, 1, 1, 1]],
              [[1],
               [1],
               [1],
               [1]],
              CYAN]
    J_TILE = [[[1, 0, 0],
               [1, 1, 1]],
              [[1, 1],
               [1, 0],
               [1, 0]],
              [[1, 1, 1],
               [0, 0, 1]],
              [[0, 1],
               [0, 1],
               [1, 1]],
              BLUE]
    L_TILE = [[[0, 0, 1],
               [1, 1, 1]],
              [[1, 0],
               [1, 0],
               [1, 1]],
              [[1, 1, 1],
               [1, 0, 0]],
              [[1, 1],
               [0, 1],
               [0, 1]],
              [255, 80, 0]]
    O_TILE = [[[1, 1],
               [1, 1]],
              [[1, 1],
               [1, 1]],
              [[1, 1],
               [1, 1]],
              [[1, 1],
               [1, 1]],
              YELLOW]
    S_TILE = [[[0, 1, 1],
               [1, 1, 0]],
              [[1, 0],
               [1, 1],
               [0, 1]],
              [[0, 1, 1],
               [1, 1, 0]],
              [[1, 0],
               [1, 1],
               [0, 1]],
              GREEN]
    T_TILE = [[[0, 1, 0],
               [1, 1, 1]],
              [[1, 0],
               [1, 1],
               [1, 0]],
              [[1, 1, 1],
               [0, 1, 0]],
              [[0, 1],
               [1, 1],
               [0, 1]],
              MAGENTA]
    Z_TILE = [[[1, 1, 0],
               [0, 1, 1]],
              [[0, 1],
               [1, 1],
               [1, 0]],
              [[1, 1, 0],
               [0, 1, 1]],
              [[0, 1],
               [1, 1],
               [1, 0]],
              RED]


####Global variables
playerName = "Anon"
hiScores = []
rndSeq = []
activeTet = ""
activeTetCoords = [0, 0]
activeTetRotation = 0
level = 1
linescleared = 0
dropPoints = 0
fixedPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(26)]
keyPressTimeout = 125
keyPressTime = 0
keyTimeout = 150
keyTime = 0
moveTimeout = 500
moveTime = 0
brightness = 1.0
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

    display.fill(gamecolors.BG_COLOR)
    display.brightness = 1.0
    display.show()


def shuffleSeq():
    str_list = [tiles.I_TILE, tiles.O_TILE, tiles.T_TILE, tiles.S_TILE, tiles.Z_TILE, tiles.J_TILE, tiles.L_TILE]
    random.shuffle(str_list)
    return str_list


def checkSpawn():
    # Check if new spawned Tetromino overlaps the current fixedPixels
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords
    tempPixels = [[0 for x in range(12)] for x in range(26)]
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][row])):
            if activeTet[activeTetRotation][row][col]:
                tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = 1
    for row in range(26):
        for col in range(12):
            if tempPixels[row][col] == 1:
                if fixedPixels[row][col] != gamecolors.BG_COLOR:
                    return True
    return False


def spawn():
    global running, rndSeq, activeTet, activeTetRotation, activeTetCoords, dropPoints
    if len(rndSeq) == 0:
        rndSeq = shuffleSeq()
    activeTet = rndSeq[0]
    del rndSeq[0]
    activeTetRotation = 0
    dropPoints = 0
    if activeTet == tiles.I_TILE:
        activeTetCoords = [2, 3]
    elif activeTet == tiles.J_TILE:
        activeTetCoords = [2, 3]
    elif activeTet == tiles.L_TILE:
        activeTetCoords = [2, 3]
    elif activeTet == tiles.O_TILE:
        activeTetCoords = [2, 4]
    elif activeTet == tiles.S_TILE:
        activeTetCoords = [2, 3]
    elif activeTet == tiles.Z_TILE:
        activeTetCoords = [2, 3]
    elif activeTet == tiles.T_TILE:
        activeTetCoords = [2, 3]
    if checkSpawn():
        gameOver()


def check_move_collision(direction:str):
    if direction == "left":
        edge = 0
        offset = -1
    elif direction == "right":
        edge = 11
        offset = 1
    else:
        raise ValueError("direction not recognized")

    global fixedPixels, activeTet, activeTetRotation, activeTetCoords

    tempPixels = [[0 for x in range(12)] for x in range(26)]
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][0])):
            tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = activeTet[activeTetRotation][row][col]

    for row in range(len(tempPixels)):
        if tempPixels[row][edge]:
            return True
        for col in range(len(tempPixels[row])):
            if tempPixels[row][col]:
                if fixedPixels[row][col + offset] != gamecolors.BG_COLOR:
                    return True

    return False


def move_side(direction:str):
    if direction == "left":
        offset = -1
    elif direction == "right":
        offset = 1
    else:
        raise ValueError("direction not recognized")

    global activeTetCoords
    activeTetCoords[1] += offset
    snd_click.play()


def gameOver():
    global rndSeq, activeTet, activeTetCoords, activeTetRotation, fixedPixels, keyTimeout, keyTime, moveTimeout, moveTime, brightness, running, paused, Tetris_Points, level, keyPressTime, keyPressTimeout, linescleared, dropPoints

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
    rndSeq = []
    activeTet = ""
    activeTetCoords = [0, 0]
    activeTetRotation = 0
    linescleared = 0
    dropPoints = 0
    level = 1
    fixedPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(24)]
    keyPressTimeout = 150
    keyPressTime = 0
    keyTimeout = 100
    keyTime = 0
    moveTimeout = 200
    moveTime = 0
    brightness = 1.0
    Tetris_Points = 0
    running = False
    paused = False


def get_next_rotation(cw: bool):
    # cw i.e. clock-wise i.e. right turn
    # opposite of cw is ccw i.e. counter-clock-wise i.e. left turn
    if cw:
        next_rotation_lookup = [1, 2, 3, 0]
        return next_rotation_lookup[activeTetRotation]
    else:
        next_rotation_lookup = [1, 2, 3, 0]
        return next_rotation_lookup[activeTetRotation]


def check_no_collision(cw: bool):
    # cw i.e. clock-wise i.e. right turn
    # opposite of cw is ccw i.e. counter-clock-wise i.e. left turn
    next_rotation = get_next_rotation(cw)

    temp_pixels = [[0 for x in range(12)] for x in range(26)]
    for row in range(len(activeTet[next_rotation])):
        for col in range(len(activeTet[next_rotation][0])):
            if activeTet[next_rotation][row][col]:
                temp_pixels[activeTetCoords[0] - 1 + row][activeTetCoords[1] + 2 + col] = 1
    for row in range(26):
        for col in range(12):
            if temp_pixels[row][col]:
                if fixedPixels[row][col] != gamecolors.BG_COLOR:
                    return False
    return True


def rotateLeft():
    global fixedPixels, activeTet, activeTetCoords, activeTetRotation
    next_rotation = get_next_rotation(False)

    if activeTet == tiles.O_TILE:
        return
    if activeTet == tiles.I_TILE:
        if activeTetRotation == 0:
            if activeTetCoords[0] > 23:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 2
                activeTetCoords[0] -= 1
        elif activeTetRotation == 1:
            if activeTetCoords[1] < 2 or activeTetCoords[1] > 8:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 2
                activeTetCoords[0] += 2
        elif activeTetRotation == 2:
            if activeTetCoords[0] > 24:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 2
        elif activeTetRotation == 3:
            if activeTetCoords[1] < 1 or activeTetCoords[1] > 7:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 1
    else:
        if activeTetRotation == 0:
            if activeTetCoords[0] > 23:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 0
        elif activeTetRotation == 1:
            if activeTetCoords[1] < 1:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 1
        elif activeTetRotation == 2:
            if activeTetCoords[0] > 24:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 0
                activeTetCoords[0] -= 1
        elif activeTetRotation == 3:
            if activeTetCoords[1] > 7:
                return
            if check_no_collision(False):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 0
                activeTetCoords[0] += 0
    snd_click.play()


def rotateRight():
    global fixedPixels, activeTet, activeTetCoords, activeTetRotation
    next_rotation = get_next_rotation(True)

    if activeTet == tiles.O_TILE:
        return
    if activeTet == tiles.I_TILE:
        if activeTetRotation == 0:
            if activeTetCoords[0] > 23:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 2
                activeTetCoords[0] -= 1
        elif activeTetRotation == 1:
            if activeTetCoords[1] < 2 or activeTetCoords[1] > 8:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 2
                activeTetCoords[0] += 2
        elif activeTetRotation == 2:
            if activeTetCoords[0] > 24:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 2
        elif activeTetRotation == 3:
            if activeTetCoords[1] < 1 or activeTetCoords[1] > 7:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 1
    else:
        if activeTetRotation == 0:
            if activeTetCoords[0] > 23:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 0
        elif activeTetRotation == 1:
            if activeTetCoords[1] < 1:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 1
        elif activeTetRotation == 2:
            if activeTetCoords[0] > 24:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] += 0
                activeTetCoords[0] -= 1
        elif activeTetRotation == 3:
            if activeTetCoords[1] > 7:
                return
            if check_no_collision(True):
                activeTetRotation = next_rotation
                activeTetCoords[1] -= 0
                activeTetCoords[0] += 0
    snd_click.play()


def keyAction(pressed_key):
    global paused, keyPressTime

    if pressed_key == "UP":
        dropDown()
    if pressed_key == "DOWN":
        moveDown()
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "RIGHT":
        if not check_move_collision(direction="right"):
            move_side("right")
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "LEFT":
        if not check_move_collision(direction="left"):
            move_side("left")
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "A":
        rotateRight()
        keyPressTime = pygame.time.get_ticks()
    if pressed_key == "B":
        rotateLeft()
        keyPressTime = pygame.time.get_ticks()

    if pressed_key == "START":
        print("Game paused")
        paused = True
        pygame.mixer.music.pause()
        snd_pause.play()
    buildScreen()


def checkMoveDownCollision():
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords
    tempPixels = [[0 for x in range(12)] for x in range(27)]  # hib
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][row])):
            tempPixels[activeTetCoords[0] + 1 + row][activeTetCoords[1] + col] = activeTet[activeTetRotation][row][col]
    if any(tempPixels[26]):
        return True
    for row in range(26):
        for col in range(12):
            if tempPixels[row][col]:
                if fixedPixels[row][col] != gamecolors.BG_COLOR:
                    return True
    return False


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
    global fixedPixels, Tetris_Points, linescleared, level
    linesFinished = 0
    for row in range(26):
        if all(map(lambda x: x != gamecolors.BG_COLOR, fixedPixels[row])):
            linesFinished += 1
            fixedPixels[row] = [gamecolors.BG_COLOR] * 12
            buildScreen()
            for mrow in range(row, 0, -1):
                fixedPixels[mrow] = fixedPixels[mrow - 1]
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
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords, moveTime, running, dropPoints, Tetris_Points, level

    # Add the active tetrimino to the fixed pixels.
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][row])):
            if activeTet[activeTetRotation][row][col]:
                fixedPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = activeTet[4]

    activeTet = None
    checkFinishedLines()
    snd_tilefix.play()
    time.sleep(moveTimeout / 1000.0)
    Tetris_Points += ((21 + (3 * level)) - dropPoints)
    spawn()
    if running:
        buildScreen()
    moveTime = pygame.time.get_ticks()


def dropDown():
    global activeTetCoords, keyTime, moveTime
    while not checkMoveDownCollision():
        activeTetCoords[0] += 1
        keyTime = pygame.time.get_ticks()
        moveTime = pygame.time.get_ticks()
        buildScreen()
    fixTile()


def moveDown():
    global activeTetCoords, dropPoints
    if checkMoveDownCollision():
        fixTile()
    else:
        activeTetCoords[0] += 1
        dropPoints += 1


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
    if joystick.get_button(1):  # Button A - right red button - Rotate right
        key_pressed = "A"
    if joystick.get_button(2):  # Button B - left red button - Rotate left
        key_pressed = "B"
    if joystick.get_button(8):
        key_pressed = "SELECT"
    if joystick.get_button(9):
        # TODO start is not get_button(9)
        key_pressed = "START"

    return key_pressed


def buildScreen():
    # Overlay fixed and mobile Pixels
    global running, fixedPixels, activeTet, activeTetRotation, activeTetCoords

    if running:
        for row in range(display.width):
            for col in range(display.height):
                display.set_pixel(row, col, fixedPixels[row + 2][col])

        if activeTet is not None:
            for row in range(len(activeTet[activeTetRotation])):
                for col in range(len(activeTet[activeTetRotation][row])):
                    if activeTet[activeTetRotation][row][col]:
                        display.set_pixel(activeTetCoords[0] - 2 + row, activeTetCoords[1] + col, activeTet[4])
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
                if joystick.get_button(9):
                    print("Game resumed.")
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
                moveDown()
                moveTime = pygame.time.get_ticks()
        if running:
            buildScreen()
    print("Tetris ended.")
