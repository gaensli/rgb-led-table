#!/usr/bin/env python
import math, sys
import time
import colorsys

PIXEL_SIZE = 3
gamma = bytearray(256)
pixels = [[[255 for x in range(3)] for x in range(10)] for x in range(20)]
numMatrix = [[0 for x in range(30)] for x in xrange(8)]
numMatrix = [[0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
             [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
             [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
             [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0]]
brightness = 0.0
spidev = file("/dev/spidev0.0", "wb")


def draw():
    for row in pixels:
        for pixel in row:
            for color in pixel:
                c = int(color * brightness)
                spidev.write(chr(c & 0xFF))
    spidev.flush()
    time.sleep(0.001)


def drawsnake():
    for row in range(0, 20):
        if row % 2 == 0:
            for pixel in range(0, 10):
                for color in range(0, 3):
                    c = int(pixels[row][pixel][color] * brightness)
                    spidev.write(chr(c & 0xFF))
        else:
            for pixel in range(9, -1, -1):
                for color in range(0, 3):
                    c = int(pixels[row][pixel][color] * brightness)
                    spidev.write(chr(c & 0xFF))
        spidev.flush()
        time.sleep(0.001)


def timedisplay():
    print "Displaying Time"
    global pixels
    global brightness
    global numMatrix
    brightness = 1
    pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
    while 1:
        timestring = time.strftime("%H%M")
        zahleins = int(timestring[0])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahleins * 3) + (y - 1)] == 1:
                    pixels[y][9 - x] = [255, 0, 0]
                else:
                    pixels[y][9 - x] = [0, 0, 0]
        zahlzwei = int(timestring[1])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahlzwei * 3) + (y - 1)] == 1:
                    pixels[y + 4][9 - x] = [255, 0, 0]
                else:
                    pixels[y + 4][9 - x] = [0, 0, 0]
        zahldrei = int(timestring[2])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahldrei * 3) + (y - 1)] == 1:
                    pixels[y + 11][9 - x] = [255, 0, 0]
                else:
                    pixels[y + 11][9 - x] = [0, 0, 0]
        zahlvier = int(timestring[3])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahlvier * 3) + (y - 1)] == 1:
                    pixels[y + 15][9 - x] = [255, 0, 0]
                else:
                    pixels[y + 15][9 - x] = [0, 0, 0]
		# Punkte
        timestring = time.strftime("%S")
        if int(timestring) % 2 == 0:
            pixels[9][2] = [255, 0, 0]
            pixels[10][2] = [255, 0, 0]
            pixels[9][3] = [255, 0, 0]
            pixels[10][3] = [255, 0, 0]

            pixels[9][6] = [255, 0, 0]
            pixels[10][6] = [255, 0, 0]
            pixels[9][7] = [255, 0, 0]
            pixels[10][7] = [255, 0, 0]
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


def fadeInOut():
    print "Fading in and out..."
    global pixels
    global brightness
    brightness = 0
    while brightness < 1:
        draw()
        time.sleep(0.2)
        brightness += 0.05
    while brightness > 0:
        draw()
        time.sleep(0.2)
        brightness -= 0.05
    pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
    brightness = 1
    draw()


def colorchase():
    print "Colorchase"
    global pixels
    global brightness
    brightness = 1
    h, s, v = 0.0, 1.0, 1.0
    row = 0
    column = 0
    for led in range(0, 200):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        aktFarbe = [0.0 for x in range(3)]
        aktFarbe = round(r * 255, 0), round(g * 255, 0), round(b * 255, 0)
        pixels[row][column] = aktFarbe
        draw()
        h = h + 0.005
        if (h > 1):
            h = h - 1.
        column += 1
        if column == 10:
            column = 0
            row += 1


def colorfade():
    print "Colorfade"
    global pixels
    global brightness
    brightness = 1
    h, s, v = 0.0, 1.0, 1.0
    while 1:
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        aktFarbe = [0.0 for x in range(3)]
        aktFarbe = round(r * 255, 0), round(g * 255, 0), round(b * 255, 0)
        pixels = [[aktFarbe for x in range(10)] for x in range(20)]
        draw()
        h = h + 0.005
        if (h > 1):
            h = h - 1.


def testsequenz():
    print "Testsequence started."
    fadeInOut()
    colorchase()
    #colorfade()
    timedisplay()


if __name__ == '__main__':
    print "RGB-Table started"
    testsequenz()
