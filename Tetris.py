import pygame, pickle
import sys, random, time

from src.Beat import RGB_Table, RED, BLACK, WHITE, GREEN, BLUE, CYAN, YELLOW, MAGENTA


class gamecolors:
    I_COLOR = CYAN
    J_COLOR = BLUE
    L_COLOR = [255, 80, 0]
    O_COLOR = YELLOW
    S_COLOR = GREEN
    T_COLOR = MAGENTA
    Z_COLOR = RED
    BG_COLOR = BLACK
    TEXTCOLOR = WHITE


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
              gamecolors.I_COLOR]
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
              gamecolors.J_COLOR]
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
              gamecolors.L_COLOR]
    O_TILE = [[[1, 1],
               [1, 1]],
              [[1, 1],
               [1, 1]],
              [[1, 1],
               [1, 1]],
              [[1, 1],
               [1, 1]],
              gamecolors.O_COLOR]
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
              gamecolors.S_COLOR]
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
              gamecolors.T_COLOR]
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
              gamecolors.Z_COLOR]


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
movingPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(26)]
displayPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(24)]
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
lastPressed = "NONE"


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


# Shuffle the next bag of Tetronimos
def shuffleSeq():
    str_list = [tiles.I_TILE, tiles.O_TILE, tiles.T_TILE, tiles.S_TILE, tiles.Z_TILE, tiles.J_TILE, tiles.L_TILE]
    random.shuffle(str_list)
    return str_list


# Check if new spawned Tetromino overlaps the current fixedPixels
def checkSpawn():
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords
    tempPixels = [[0 for x in range(12)] for x in range(26)]
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][0])):
            if activeTet[activeTetRotation][row][col]:
                tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = 1
    for row in range(26):
        for col in range(12):
            if tempPixels[row][col] == 1:
                if fixedPixels[row][col] != gamecolors.BG_COLOR:
                    return True
    return False


# Spawn a new Tetromino
def resetGame():
    global rndSeq, activeTet, activeTetCoords, activeTetRotation, fixedPixels, movingPixels, displayPixels, keyTimeout, keyTime, moveTimeout, moveTime, brightness, running, Tetris_Points, lastPressed, level, keyPressTime, keyPressTimeout, linescleared, dropPoints
    rndSeq = []
    activeTet = ""
    activeTetCoords = [0, 0]
    activeTetRotation = 0
    linescleared = 0
    dropPoints = 0
    level = 1
    fixedPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(24)]
    movingPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(24)]
    displayPixels = [[gamecolors.BG_COLOR for x in range(12)] for x in range(24)]
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
    lastPressed = "NONE"


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
        resetGame()


def checkMoveLeftCollision():
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords
    tempPixels = [[0 for x in range(12)] for x in range(26)]
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][0])):
            if activeTet[activeTetRotation][row][col]:
                tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = 1
    for row in range(26):
        if tempPixels[row][0] == 1:
            return True
    for row in range(26):
        for col in range(12):
            if tempPixels[row][col] == 1:
                if fixedPixels[row][col - 1] != gamecolors.BG_COLOR:
                    return True
    return False


def checkMoveRightCollision():
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords
    tempPixels = [[0 for x in range(12)] for x in range(26)]
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][0])):
            if activeTet[activeTetRotation][row][col]:
                tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = 1
    for row in range(26):
        if tempPixels[row][11] == 1:
            return True
    for row in range(26):
        for col in range(12):
            if tempPixels[row][col] == 1:
                if fixedPixels[row][col + 1] != gamecolors.BG_COLOR:
                    return True
    return False


def moveRight():
    global activeTetCoords
    activeTetCoords[1] += 1
    snd_click.play()


def moveLeft():
    global activeTetCoords
    activeTetCoords[1] -= 1
    snd_click.play()


# Player is gameover
def gameOver():
    print("Game over. " + str(Tetris_Points) + " points.")
    pygame.mixer.music.stop()
    snd_gameover.play()
    time.sleep(3)
    fadeInOut([255, 0, 0])
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # sock.sendto(str(Tetris_Points), ("192.168.0.241", 56565))
    entry = (playerName, Tetris_Points)
    hiScores.append(entry)
    hiScores.sort(key=getKey, reverse=True)
    pickle.dump(hiScores, open("/home/pi/rgb-led-table/hiscores.zfl", "wb"))


# Teil nach links drehen
def rotateLeft():
    global fixedPixels, activeTet, activeTetCoords, activeTetRotation
    if activeTet == tiles.I_TILE:
        validMove = True
        if activeTetRotation == 0:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 23:
                validMove = False
            else:
                for row in range(len(activeTet[3])):
                    for col in range(len(activeTet[3][0])):
                        if activeTet[3][row][col]:
                            tempPixels[activeTetCoords[0] - 1 + row][activeTetCoords[1] + 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 3
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 1
        elif activeTetRotation == 3:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] < 1 or activeTetCoords[1] > 7:  # hib
                validMove = False
            else:
                for row in range(len(activeTet[2])):
                    for col in range(len(activeTet[2][0])):
                        if activeTet[2][row][col]:
                            tempPixels[activeTetCoords[0] + 2 + row][activeTetCoords[1] - 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 2
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 2
        elif activeTetRotation == 2:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 24:
                validMove = False
            else:
                for row in range(len(activeTet[1])):
                    for col in range(len(activeTet[1][0])):
                        if activeTet[1][row][col]:
                            tempPixels[activeTetCoords[0] - 2 + row][activeTetCoords[1] + 2 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 1
                activeTetCoords[1] += 2
                activeTetCoords[0] -= 2
        elif activeTetRotation == 1:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] < 2 or activeTetCoords[1] > 8:
                validMove = False
            else:
                for row in range(len(activeTet[0])):
                    for col in range(len(activeTet[0][0])):
                        if activeTet[0][row][col]:
                            tempPixels[activeTetCoords[0] + 1 + row][activeTetCoords[1] - 2 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 0
                activeTetCoords[1] -= 2
                activeTetCoords[0] += 1
    elif activeTet == tiles.J_TILE or activeTet == tiles.L_TILE or activeTet == tiles.S_TILE or activeTet == tiles.T_TILE or activeTet == tiles.Z_TILE:
        validMove = True
        if activeTetRotation == 0:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 23:
                validMove = False
            else:
                for row in range(len(activeTet[3])):
                    for col in range(len(activeTet[3][0])):
                        if activeTet[3][row][col]:
                            tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 3
                activeTetCoords[1] += 0
                activeTetCoords[0] -= 0
        elif activeTetRotation == 3:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] > 7:
                validMove = False
            else:
                for row in range(len(activeTet[2])):
                    for col in range(len(activeTet[2][0])):
                        if activeTet[2][row][col]:
                            tempPixels[activeTetCoords[0] + 1 + row][activeTetCoords[1] + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 2
                activeTetCoords[1] -= 0
                activeTetCoords[0] += 1
        elif activeTetRotation == 2:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 24:
                validMove = False
            else:
                for row in range(len(activeTet[1])):
                    for col in range(len(activeTet[1][0])):
                        if activeTet[1][row][col]:
                            tempPixels[activeTetCoords[0] - 1 + row][activeTetCoords[1] + 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 1
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 1
        elif activeTetRotation == 1:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] < 1:
                validMove = False
            else:
                for row in range(len(activeTet[0])):
                    for col in range(len(activeTet[0][0])):
                        if activeTet[0][row][col]:
                            tempPixels[activeTetCoords[0] + 0 + row][activeTetCoords[1] - 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 0
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 0
    elif activeTet == tiles.O_TILE:
        return False
    snd_click.play()


# Teil nach rechts drehen
def rotateRight():
    global fixedPixels, activeTet, activeTetCoords, activeTetRotation
    if activeTet == tiles.I_TILE:
        validMove = True
        if activeTetRotation == 0:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 23:
                validMove = False
            else:
                for row in range(len(activeTet[1])):
                    for col in range(len(activeTet[1][0])):
                        if activeTet[1][row][col]:
                            tempPixels[activeTetCoords[0] - 1 + row][activeTetCoords[1] + 2 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 1
                activeTetCoords[1] += 2
                activeTetCoords[0] -= 1
        elif activeTetRotation == 1:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] < 2 or activeTetCoords[1] > 8:
                validMove = False
            else:
                for row in range(len(activeTet[2])):
                    for col in range(len(activeTet[2][0])):
                        if activeTet[2][row][col]:
                            tempPixels[activeTetCoords[0] + 2 + row][activeTetCoords[1] - 2 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 2
                activeTetCoords[1] -= 2
                activeTetCoords[0] += 2
        elif activeTetRotation == 2:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 24:
                validMove = False
            else:
                for row in range(len(activeTet[3])):
                    for col in range(len(activeTet[3][0])):
                        if activeTet[3][row][col]:
                            tempPixels[activeTetCoords[0] - 2 + row][activeTetCoords[1] + 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 3
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 2
        elif activeTetRotation == 3:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] < 1 or activeTetCoords[1] > 7:
                validMove = False
            else:
                for row in range(len(activeTet[0])):
                    for col in range(len(activeTet[0][0])):
                        if activeTet[0][row][col]:
                            tempPixels[activeTetCoords[0] + 1 + row][activeTetCoords[1] - 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 0
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 1
    elif activeTet == tiles.J_TILE or activeTet == tiles.L_TILE or activeTet == tiles.S_TILE or activeTet == tiles.T_TILE or activeTet == tiles.Z_TILE:
        validMove = True
        if activeTetRotation == 0:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 23:
                validMove = False
            else:
                for row in range(len(activeTet[1])):
                    for col in range(len(activeTet[1][0])):
                        if activeTet[1][row][col]:
                            tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 1
                activeTetCoords[1] += 1
                activeTetCoords[0] -= 0
        elif activeTetRotation == 1:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] < 1:
                validMove = False
            else:
                for row in range(len(activeTet[2])):
                    for col in range(len(activeTet[2][0])):
                        if activeTet[2][row][col]:
                            tempPixels[activeTetCoords[0] + 1 + row][activeTetCoords[1] - 1 + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 2
                activeTetCoords[1] -= 1
                activeTetCoords[0] += 1
        elif activeTetRotation == 2:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[0] > 24:
                validMove = False
            else:
                for row in range(len(activeTet[3])):
                    for col in range(len(activeTet[3][0])):
                        if activeTet[3][row][col]:
                            tempPixels[activeTetCoords[0] - 1 + row][activeTetCoords[1] + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 3
                activeTetCoords[1] += 0
                activeTetCoords[0] -= 1
        elif activeTetRotation == 3:
            tempPixels = [[0 for x in range(12)] for x in range(26)]
            if activeTetCoords[1] > 7:
                validMove = False
            else:
                for row in range(len(activeTet[0])):
                    for col in range(len(activeTet[0][0])):
                        if activeTet[0][row][col]:
                            tempPixels[activeTetCoords[0] + row][activeTetCoords[1] + col] = 1
                for row in range(26):
                    for col in range(12):
                        if tempPixels[row][col] == 1:
                            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                                validMove = False
            if validMove:
                activeTetRotation = 0
                activeTetCoords[1] -= 0
                activeTetCoords[0] += 0
    elif activeTet == tiles.O_TILE:
        return False
    snd_click.play()


# Process inputs
def keyAction():
    global lastPressed, paused, keyPressTime

    if lastPressed == "UP":
        dropDown()
    if lastPressed == "DOWN":
        moveDown()
        keyPressTime = pygame.time.get_ticks()
    if lastPressed == "RIGHT":
        if not checkMoveRightCollision():
            moveRight()
            keyPressTime = pygame.time.get_ticks()
    if lastPressed == "LEFT":
        if not checkMoveLeftCollision():
            moveLeft()
            keyPressTime = pygame.time.get_ticks()
    if lastPressed == "A":
        rotateRight()
        keyPressTime = pygame.time.get_ticks()
    if lastPressed == "B":
        rotateLeft()
        keyPressTime = pygame.time.get_ticks()
    if lastPressed == "SELECT":
        print("Button 8 - Select button")
    if lastPressed == "START":
        print("Game paused")
        paused = True
        pygame.mixer.music.pause()
        snd_pause.play()
    buildScreen()
    lastPressed = "NONE"


def checkMoveDownCollision():
    global fixedPixels, activeTet, activeTetRotation, activeTetCoords
    tempPixels = [[0 for x in range(12)] for x in range(27)]  # hib
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][0])):
            if activeTet[activeTetRotation][row][col]:
                tempPixels[activeTetCoords[0] + 1 + row][activeTetCoords[1] + col] = 1
    for col in range(0, 12):
        if tempPixels[26][col] == 1:
            return True
    for row in range(26):
        for col in range(12):
            if tempPixels[row][col] == 1:
                if fixedPixels[row][col] != gamecolors.BG_COLOR:
                    return True
    return False


def setLevelAndSpeed(lines):
    global linescleared, level, moveTimeout, Tetris_Points
    prelevel = level
    if linescleared <= 0:
        level = 1
    elif linescleared >= 1 and linescleared <= 90:
        level = 1 + ((linescleared - 1) / 10)
    elif linescleared >= 91:
        level = 10

    if level > prelevel:
        snd_level.play()
    moveTimeout = (((11 - level) * 50))
    print("Abgeraeumte Linien: " + str(linescleared) + " - Level: " + str(level) + " - moveTime: " + str(
        moveTimeout) + " - Tetris Points: " + str(Tetris_Points))


def checkFinishedLines():
    global fixedPixels, Tetris_Points, linescleared, level
    linesFinished = 0
    for row in range(26):
        counter = 0
        for col in range(12):
            if fixedPixels[row][col] != gamecolors.BG_COLOR:
                counter += 1
        if counter == 12:
            linesFinished += 1
            for col in range(12):
                fixedPixels[row][col] = gamecolors.BG_COLOR
            buildScreen()
            for mrow in range(row, 0, -1):
                for mcol in range(12):
                    fixedPixels[mrow][mcol] = fixedPixels[mrow - 1][mcol]
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
    for row in range(len(activeTet[activeTetRotation])):
        for col in range(len(activeTet[activeTetRotation][0])):
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


# Let gravity pull the mobile pixels down
def timeAction():
    global activeTetCoords, dropPoints
    if checkMoveDownCollision():
        fixTile()
    else:
        activeTetCoords[0] += 1
        dropPoints += 1


def moveDown():
    global activeTetCoords, moveTime, dropPoints
    if checkMoveDownCollision():
        fixTile()
    else:
        activeTetCoords[0] += 1
        dropPoints += 1


def getKeypress(u):
    global lastPressed
    pygame.event.pump()
    if u.get_axis(1) <= -0.5:  # D-Pad nach oben
        lastPressed = "UP"
    if u.get_axis(1) >= +0.5:  # D-Pad nach unten
        lastPressed = "DOWN"
    if u.get_axis(0) >= +0.5:  # D-Pad rechts
        lastPressed = "RIGHT"
    if u.get_axis(0) <= -0.5:  # D-Pad nach links
        lastPressed = "LEFT"
    if u.get_button(1):  # Button A - right red button - Rotate right
        lastPressed = "A"
    if u.get_button(2):  # Button B - left red button - Rotate left
        lastPressed = "B"
    if u.get_button(8):
        lastPressed = "SELECT"
    if u.get_button(9):
        lastPressed = "START"


# Overlay fixed and mobile Pixels
def buildScreen():
    global running, displayPixels, fixedPixels, activeTet, activeTetRotation, activeTetCoords
    if running:
        for row in range(24):
            for pixel in range(12):
                display.set_pixel(row, pixel, fixedPixels[row + 2][pixel])
        if activeTet != None:
            for row in range(len(activeTet[activeTetRotation])):
                for col in range(len(activeTet[activeTetRotation][0])):
                    if activeTet[activeTetRotation][row][col]:
                        display.set_pixel(activeTetCoords[0] - 2 + row, activeTetCoords[1] + col, activeTet[4])
        display.show()


def getKey(item):
    return item[1]


# Main loop to control the game
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

    j = pygame.joystick.Joystick(0)
    j.init()
    print(f'Initialized Joystick : {j.get_name()}')

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

    while running:
        if paused:
            time.sleep(1)
            while paused:
                pygame.event.pump()
                if j.get_button(9):
                    print("Game unpaused")
                    snd_pause.play()
                    pygame.mixer.music.unpause()
                    time.sleep(1)
                    paused = False
                    lastPressed = "NONE"

        if running:
            if pygame.time.get_ticks() > keyPressTime + keyPressTimeout:
                getKeypress(j)
            if pygame.time.get_ticks() > keyTime + keyTimeout:
                keyAction()
                keyTime = pygame.time.get_ticks()
            if pygame.time.get_ticks() > moveTime + moveTimeout:
                timeAction()
                moveTime = pygame.time.get_ticks()
        if running:
            buildScreen()
    print("Tetris ended.")
