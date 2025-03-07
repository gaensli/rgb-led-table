#!/usr/bin/python
import math, sys
import time
import socket

class StartClass:
    spidev = file("/dev/spidev0.0", "wb")    
    def __init__(self):
        self.brightness = 1.0
        self.displayPixels = [[[0,0,0] for x in range(10)] for x in range(20)]        
    def draw(self,matrix):
        sendstring = ""
        for row in range(20):
            if row%2==0:
                for pixel in range(0,10):
                    for color in range(0,3):
                        c=int(matrix[row][pixel][color]*self.brightness)
                        sendstring += chr(c & 0xFF)
            else:
                for pixel in range(9,-1,-1):
                    for color in range(0,3):
                        c=int(matrix[row][pixel][color]*self.brightness)
                        sendstring += chr(c & 0xFF)            
        self.spidev.write(sendstring)        
        self.spidev.flush()
        time.sleep(0.001)
    def fadeInOut(self,c):
            self.brightness=0.0
            self.displayPixels = [[c for x in range(10)] for x in range(20)]
            while self.brightness <1.0:
                    self.draw(self.displayPixels)
                    self.brightness+=0.05
            while self.brightness >0.0:
                    self.draw(self.displayPixels)
                    self.brightness-=0.05
            self.displayPixels = [[[0,0,0] for x in range(10)] for x in range(20)]
            self.brightness = 1.0
            self.draw(self.displayPixels)
    def flashBlue(self):
        self.fadeInOut([0,0,255])        