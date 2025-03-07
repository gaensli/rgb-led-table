#!/usr/bin/env python
import math, sys
import time, random
import colorsys

PIXEL_SIZE = 3
gamma = bytearray(256)
pixels = [[[0 for x in range(3)] for x in range(24)] for x in range(12)]
brightness = 1.0
spidev = file("/dev/spidev0.0", "wb")

def draw():
        for row in pixels:
                for pixel in row:
                        for color in pixel:
                                c = int(color*brightness)
                                spidev.write(chr(c & 0xFF))
        spidev.flush()
        time.sleep(0.001)

def initScreen():
    global pixels
    for row in range(0,11):
        for pixel in range(0,23):
            pixels[row][pixel]=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    draw()
def changePixels():
    global pixels
    pixels[random.randint(0,11)][random.randint(0,23)] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    draw()
if __name__ == '__main__':
    print("Random pixels")
    initScreen()
    while 1:
        changePixels()