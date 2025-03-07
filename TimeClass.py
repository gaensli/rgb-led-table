#!/usr/bin/env python
import math, sys
import time, socket
import colorsys
from random import randint

class TimedisplayClass:
    spidev = file("/dev/spidev0.0", "wb")    
    def __init__(self,s):
        self.pixels = [[[255 for x in range(3)] for x in range(12)] for x in range(24)]
        self.numMatrix = [[0 for x in range(30)] for x in xrange(8)]
        self.numMatrix = [[0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
                     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
                     [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                     [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0]]
        self.brightness = 0.5
        #self.pixels = [[[0 for x in range(3)] for x in range(12)] for x in range(24)]
        #self.numMatrix = [[0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,0,1,0],[1,0,1,1,1,0,1,0,1,0,0,1,1,0,1,1,0,0,1,0,0,0,0,1,1,0,1,1,0,1],[1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,0,0,1,0,0,0,0,1,1,0,1,1,0,1],[1,0,1,0,1,0,0,0,1,0,1,0,1,1,1,1,1,0,1,1,0,0,1,0,0,1,0,0,1,1],[1,0,1,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,0,1],[1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1],[1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1],[0,1,0,1,1,1,1,1,1,0,1,0,0,0,1,1,1,0,0,1,0,1,0,0,0,1,0,1,1,0]]
        #self.brightness = 1.0
        self.running = True
        self.s = s
    def drawsnake(self):
        print("arschloch")
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
    def timeStart(self):
        print("Time started")
        while self.running:
            try:
                data = self.s.recv(1024)
                if data=="AbOrTTrObA":
                    self.running=False
            except: 
                pass
            timestring = time.strftime("%H%M")
            zahleins = int(timestring[0])
            color1 = 255
            color3 = 30
            color2 = 0
            for x in range(1, 9):
                for y in range(1, 4):
                    print("scheisse")
                    if self.numMatrix[(x - 1)][(zahleins * 3) + (y - 1)] == 1:
                        self.pixels[y][9 - x] = [color1, color2, color3]
                    else:
                        self.pixels[y][9 - x] = [0, 0, 0]
            zahlzwei = int(timestring[1])
            for x in range(1, 9):
                for y in range(1, 4):
                    if self.numMatrix[(x - 1)][(zahlzwei * 3) + (y - 1)] == 1:
                        self.pixels[y + 4][9 - x] = [color1, color2, color3]
                    else:
                        self.pixels[y + 4][9 - x] = [0, 0, 0]
            zahldrei = int(timestring[2])
            for x in range(1, 9):
                for y in range(1, 4):
                    if self.numMatrix[(x - 1)][(zahldrei * 3) + (y - 1)] == 1:
                        self.pixels[y + 11][9 - x] = [color1, color2, color3]
                    else:
                        self.pixels[y + 11][9 - x] = [0, 0, 0]
            zahlvier = int(timestring[3])
            for x in range(1, 9):
                for y in range(1, 4):
                    if self.numMatrix[(x - 1)][(zahlvier * 3) + (y - 1)] == 1:
                        self.pixels[y + 15][9 - x] = [color1, color2, color3]
                    else:
                        self.pixels[y + 15][9 - x] = [0, 0, 0]
            # Punkte
            timestring = time.strftime("%S")
            if int(timestring) % 2 == 0:
                num = randint(0, 255)
                self.pixels[9][2] = [num, num, num]
                self.pixels[10][2] = [num, num, num]
                self.pixels[9][3] = [num, num, num]
                self.pixels[10][3] = [num, num, num]

                self.pixels[9][6] = [num, num, num]
                self.pixels[10][6] = [num, num, num]
                self.pixels[9][7] = [num, num, num]
                self.pixels[10][7] = [num, num, num]
            else:
                self.pixels[9][2] = [0, 0, 0]
                self.pixels[10][2] = [0, 0, 0]
                self.pixels[9][3] = [0, 0, 0]
                self.pixels[10][3] = [0, 0, 0]

                self.pixels[9][6] = [0, 0, 0]
                self.pixels[10][6] = [0, 0, 0]
                self.pixels[9][7] = [0, 0, 0]
                self.pixels[10][7] = [0, 0, 0]
            self.drawsnake()
            time.sleep(1)
        print("Time closed")