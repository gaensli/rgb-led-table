#!/usr/bin/env python
import math, sys
import time, random
import colorsys
import pygame
from pygame.locals import *
from colorsys import hsv_to_rgb, rgb_to_hsv


pixels = [[[0 for x in range(3)] for x in range(12)] for x in range(24)]
brightness = 1.0
waittime = 0.001
spidev = file("/dev/spidev0.0", "wb")
def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in hsv_to_rgb(h,s,v))
def rgb2hsv(r,g,b):
    return tuple(i  for i in rgb_to_hsv(r/ 255.0, g/ 255.0, b/ 255.0))
def draw():
        for row in pixels:
                for pixel in row:
                        for color in pixel:
                                c = int(color*brightness)
                                spidev.write(chr(c & 0xFF))
        spidev.flush()
        time.sleep(waittime)
def initScreen():
    global pixels
    global brightness
    for row in range(0,24):
        for pixel in range(0,12):
            r, g, b = hsv2rgb(random.uniform(0.0,0.18),1,1)
            pixels[row][pixel]=[r*brightness,g*brightness,b*brightness]
    draw()
def changePixels():
    global pixels
    global brightness
    for row in range(0,24):
        for col in range(0,12):
            #r, g, b = hsv2rgb(random.uniform(0.0,0.18),1,1)
            r, g, b = hsv2rgb(random.uniform(0.0,0.18),random.uniform(0.0,0.18),random.uniform(0.0,0.18))
            pixels[row][col] = [r*brightness,g*brightness,b*brightness]
    draw() 
if __name__ == '__main__':
    pygame.quit()
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print ("Error, I did not find any joysticks")
    else:
        j = pygame.joystick.Joystick(0)
        j.quit()
        j.init()
        print 'Initialized Joystick : %s' % j.get_name()
    initScreen()
    while 1:
        pygame.display
        pygame.event.pump()


        if j.get_axis(1) <= -0.5:
            if brightness <= 0.99:
                brightness +=0.01
                print 'Brightness : %s' % brightness
                
        if j.get_axis(1) >= +0.5:
            if brightness >= 0.01:
                brightness -=0.01
                print("axis1")

        if j.get_axis(0) >= +0.5:
            if waittime <= 99.981:
                waittime +=0.02
                print("axis0 > 0.5")
               
        if j.get_axis(0) <= -0.5:
            if waittime >= 0.021:
                waittime -=0.02
                print("axis0 < 0.5")

        if j.get_button(1):
            waittime = 0.001
            brightness = 1.0
            print("button")

        global lastPressed
        lastPressed = "nix"

        if j.get_axis(1) <= -0.5:  # D-Pad nach oben
            lastPressed = "UP"
        if j.get_axis(1) >= +0.5:  # D-Pad nach unten
            lastPressed = "DOWN"
        if j.get_axis(0) >= +0.5:  # D-Pad rechts
            lastPressed = "RIGHT"
        if j.get_axis(0) <= -0.5:  # D-Pad nach links
            lastPressed = "LEFT"
        if j.get_button(1):  # Button A - right red button - Rotate right
            lastPressed = "A"
        if j.get_button(2):  # Button B - left red button - Rotate left
            lastPressed = "B"
        if j.get_button(8):
            lastPressed = "SELECT"
        if j.get_button(9):
            lastPressed = "START"

        print(lastPressed)
        changePixels()
