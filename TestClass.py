#!/usr/bin/env python
import math, sys
import time, socket
class TestAnimationClass:
    spidev = file("/dev/spidev0.0", "wb")    
    def __init__(self,s):   
        self.pixels = [[[255 for x in range(3)] for x in range(12)] for x in range(24)]
        self.brightness = 1.0
        self.running = True
        self.s = s
        self.Color = [255,255,255]
    def draw(self):
        print("draw TES")
        for row in range(0,12):
            if row%2==0:
                for pixel in range(0,24):
                    for color in range(0,3):
                        c=int(self.pixels[pixel][row][color]*self.brightness)
                        self.spidev.write(chr(c & 0xFF))
            else:
                for pixel in range(23,-1,-1):
                    for color in range(0,3):
                        c=int(self.pixels[pixel][row][color]*self.brightness)
                        self.spidev.write(chr(c & 0xFF))
        self.spidev.flush()
        time.sleep(0.001)
    def testStart(self):
        print("Test Animation started")
        while self.running:
            try:
                data = self.s.recv(1024)
                if data=="AbOrTTrObA":
                        self.running=False
            except:
                pass

            for x in range (0,24):
                for y in range (0,12):
                    if self.Color==[255,255,255]:
                        self.Color=[255,0,0]
                    elif self.Color==[255,0,0]:
                        self.Color=[0,255,0]
                    elif self.Color==[0,255,0]:
                        self.Color=[0,0,255]
                    elif self.Color==[0,0,255]:
                        self.Color=[255,255,255]
                    self.pixels[x][y] = self.Color
            self.draw()
            time.sleep(1.0)
        print("Test Animation closed")