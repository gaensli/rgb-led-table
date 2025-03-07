#!/usr/bin/env python
import math, sys
import time, random
import colorsys
import pygame
from pygame.locals import *
from colorsys import hsv_to_rgb, rgb_to_hsv

fromcolor = 0.0
tocolor = 0.0
pixels = [[[0 for x in range(3)] for x in range(12)] for x in range(24)]
brightness = 0.1
waittime = 50
waitbright = 200
waitint = 100
REFRESHSCREEN = USEREVENT+1
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
        time.sleep(0.01)
def initScreen():
    global pixels
    global brightness
    for row in range(0,24):
        for pixel in range(0,12):
            r, g, b = hsv2rgb(random.uniform(fromcolor,tocolor),random.random(),1)
            pixels[row][pixel]=[r,g,b]
    draw()
def changePixels():
    global pixels
    global brightness
    for i in range(0,5):
        row = random.randint(0,23)
        col = random.randint(0,11)
        r, g, b = hsv2rgb(random.uniform(fromcolor,tocolor),1,1000)
        pixels[row][col] = [r,g,b]
    draw() 
if __name__ == '__main__':
    fromcolor = float(sys.argv[1])/360
    tocolor = float(sys.argv[2])/360
    pygame.quit()
    print("Random blue pixels")
    pygame.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print ("Error, I did not find any joysticks")
    else:
        j = pygame.joystick.Joystick(0)
        j.quit()
        j.init()
        pygame.joystick.Joystick(0)
        print 'Initialized Joystick : %s' % j.get_name()
        print 'Joystick buttons : %s' % j.get_numbuttons()
    initScreen()
    pygame.time.set_timer(REFRESHSCREEN, waittime)
    cl = pygame.time.Clock()
    start = pygame.time.get_ticks()
    startbright = start
    startint = start
    while 1:
        pygame.event.pump()
        #Check if waitbright-Intervall has passed since last change of brightness and update if buttons pressed
        if (pygame.time.get_ticks()>=startbright+waitbright):
            if j.get_axis(1) <= -0.5:
                if brightness <= 0.95:
                    brightness +=0.05
                    
            if j.get_axis(1) >= +0.5:
                if brightness >= 0.05:
                    brightness -=0.05
            draw()
            startbright = pygame.time.get_ticks()
                        
        if (pygame.time.get_ticks()>=startint+waitint):
            if j.get_axis(0) >= +0.5:
                if waittime <= 9980:
                    waittime +=20
                   
            if j.get_axis(0) <= -0.5:
                if waittime >= 20:
                    waittime -=20
            startint = pygame.time.get_ticks()

        if j.get_button(0):
            print("Button 0")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(1):
            print("Button 1")
            waittime = 1
            brightness = 1.0
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(2):
            print("Button 2")
            waittime = 1
            brightness = 0.1
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(3):
            print("Button 3")
            waittime = 1
            brightness = 0.5
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(4):
            print("Button 4")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(5):
            print("Button 5")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(6):
            print("Button 6")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(7):
            print("Button 7")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()

        if j.get_button(8):
            print("Button 8")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()
        if j.get_button(9):
            print("Button 9")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()
        if j.get_button(10):
            print("Button 10")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()
        if j.get_button(11):
            print("Button 11")
            waittime = 1
            brightness = 0.25
            startint = pygame.time.get_ticks()
            changePixels()


        if (pygame.time.get_ticks()>=start+waittime):
                changePixels()
                start = pygame.time.get_ticks()