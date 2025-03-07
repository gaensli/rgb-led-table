#!/usr/bin/env python
import math, sys
import time, random
import colorsys
from colorsys import hsv_to_rgb, rgb_to_hsv

pixels = [[[0 for x in range(3)] for x in range(12)] for x in range(24)]
brightness = 0.6
reverse = 1
spidev = file("/dev/spidev0.0", "wb")
def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
def rgb2hsv(r,g,b):
    return tuple(i  for i in colorsys.rgb_to_hsv(r/ 255.0, g/ 255.0, b/ 255.0))
def draw():
        for row in pixels:
                for pixel in row:
                        for color in pixel:
                                c = int(color*brightness)
                                spidev.write(chr(c & 0xFF))
        spidev.flush()
        time.sleep(0.1)
def initScreen():
    global pixels
    brightness = 0.6
    for row in range(0,24):
        for pixel in range(0,12):
            r, g, b = hsv2rgb(random.uniform(0.9,1.0),1,2)
            pixels[row][pixel]=[r*brightness,g*brightness,b*brightness]
            print("init")
    draw()
def changePixels():
    global pixels
    global brightness
    global reverse


    row = random.randint(0,23)
    col = random.randint(0,11)
    r, g, b = hsv2rgb(random.uniform(0.1,1.0),1,1)
    old = pixels[row][col]
    ho,so,vo = rgb2hsv(old[0],old[1],old[2])
    hn,sn,vn = rgb2hsv(r,g,b)
    diff = hn-ho
    for i in range(0,24):
        r, g, b = hsv2rgb((ho+(diff/24*(i+1))),1,0.5)
        #if not reverse:
        #    brightness += 0.01
        #else:
        #    brightness -= 0.01


        pixels[row][col] = [r*brightness,g*brightness,b*brightness]
        draw()
    #reverse = 0

if __name__ == '__main__':
    print("Random pixels")
    initScreen()
    while 1:
        changePixels()