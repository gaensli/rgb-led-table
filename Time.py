#!/usr/bin/env python
import math, sys
import time
import colorsys
from random import randint

pixels = [[[255 for x in range(3)] for x in range(12)] for x in range(24)]
numMatrix = [[0 for x in range(30)] for x in xrange(8)]
numMatrix = [[0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
             [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
             [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
             [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0]]
brightness = 0.5
spidev = file("/dev/spidev0.0", "wb")


def drawsnake():
    for row in range(0, 12):
        if row % 2 == 0:
            for pixel in range(0, 24):
                for col in range(0, 3):
                    c = int(pixels[pixel][row][col] * brightness)
                    spidev.write(chr(c & 0xFF))
        else:
            for pixel in range(23, -1, -1):
                for col in range(0, 3):
                    c = int(pixels[pixel][row][col] * brightness)
                    spidev.write(chr(c & 0xFF))
    spidev.flush()
    # time.sleep(0.001)


def timedisplay():
    global pixels
    global brightness
    global numMatrix
    brightness = 0.5
    pixels = [[[0 for x in range(3)] for x in range(12)] for x in range(24)]

    while 1:
        timestring = time.strftime("%H%M")
        zahleins = int(timestring[0])
        color1 = 255
        color3 = 30
        color2 = 0
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahleins * 3) + (y - 1)] == 1:
                    pixels[y][9 - x] = [color1, color2, color3]
                else:
                    pixels[y][9 - x] = [0, 0, 0]
        zahlzwei = int(timestring[1])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahlzwei * 3) + (y - 1)] == 1:
                    pixels[y + 4][9 - x] = [color1, color2, color3]
                else:
                    pixels[y + 4][9 - x] = [0, 0, 0]
        zahldrei = int(timestring[2])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahldrei * 3) + (y - 1)] == 1:
                    pixels[y + 11][9 - x] = [color1, color2, color3]
                else:
                    pixels[y + 11][9 - x] = [0, 0, 0]
        zahlvier = int(timestring[3])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahlvier * 3) + (y - 1)] == 1:
                    pixels[y + 15][9 - x] = [color1, color2, color3]
                else:
                    pixels[y + 15][9 - x] = [0, 0, 0]
        # Punkte
        timestring = time.strftime("%S")
        if int(timestring) % 2 == 0:
            num = randint(0, 255)
            pixels[9][2] = [num, num, num]
            pixels[10][2] = [num, num, num]
            pixels[9][3] = [num, num, num]
            pixels[10][3] = [num, num, num]

            pixels[9][6] = [num, num, num]
            pixels[10][6] = [num, num, num]
            pixels[9][7] = [num, num, num]
            pixels[10][7] = [num, num, num]
        else:
            pixels[9][2] = [0, 0, 0]
            pixels[10][2] = [0, 0, 0]
            pixels[9][3] = [0, 0, 0]
            pixels[10][3] = [0, 0, 0]

            pixels[9][6] = [0, 0, 0]
            pixels[10][6] = [0, 0, 0]
            pixels[9][7] = [0, 0, 0]
            pixels[10][7] = [0, 0, 0]
        drawsnake()
        time.sleep(1)


if __name__ == '__main__':
    timedisplay()
