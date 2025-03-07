#!/usr/bin/env python
import math, sys
import time, random
import colorsys

from colorsys import hsv_to_rgb, rgb_to_hsv

pixels = [[[0 for x in range(3)] for x in range(12)] for x in range(24)]
brightness = 1.0
spidev = file("/dev/spidev0.0", "wb")


def hsv2rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def rgb2hsv(r, g, b):
    return tuple(i for i in colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0))


def draw():
    for row in pixels:
        for pixel in row:
            for color in pixel:
                c = int(color * brightness)
                spidev.write(chr(c & 0xFF))
    spidev.flush()
    #time.sleep(2.5)


def initScreen():
    global pixels
    for row in range(0, 23):
        for pixel in range(0, 11):
            r, g, b = hsv2rgb(random.random(), 1, 1)
            pixels[row][pixel] = [r * brightness, g * brightness, b * brightness]
    draw()


def changePixels():
    global pixels
    row = random.randint(0, 23)
    col = random.randint(0, 11)
    r, g, b = hsv2rgb(random.random(), 1, 1)
    pixels[row][col] = [r * brightness, g * brightness, b * brightness]
    draw()


if __name__ == '__main__':
    print("Random pixels")
    initScreen()
    while 1:
        changePixels()
