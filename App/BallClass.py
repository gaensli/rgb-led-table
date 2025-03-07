#!/usr/bin/env python
import math, sys
import time, socket, random
import colorsys
class BallanimationClass:
    spidev = file("/dev/spidev0.0", "wb")    
    def __init__(self,s):   
        self.pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
        self.brightness = 0.1
        self.running = True
        self.s = s
	self.Pos = [0,0]
	self.Dir = 0 # 0=top-right,1=bottom-right,2=top-left,3=bottom-left
	self.Color = [255,255,255]
    def draw(self):
        for row in range(0,20):
            if row%2==0:
                for pixel in range(0,10):
                    for color in range(0,3):
                        c=int(self.pixels[row][pixel][color]*self.brightness)
                        self.spidev.write(chr(c & 0xFF))
            else:
                for pixel in range(9,-1,-1):
                    for color in range(0,3):
                        c=int(self.pixels[row][pixel][color]*self.brightness)
                        self.spidev.write(chr(c & 0xFF))            
        self.spidev.flush()
        time.sleep(0.001)
    def ballStart(self):
        print("Ball Animation started")
	self.Pos = [random.randint(0, 19),random.randint(0, 9)]
	self.Dir=random.randint(0, 3)
	self.Color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
	for x in range (0,20):
        	for y in range (0,10):
        		self.pixels[x][y]=[0,0,0]     
	self.pixels[self.Pos[0]][self.Pos[1]]=self.Color

        while self.running:
            	try:
                	data = self.s.recv(1024)
                	if data=="AbOrTTrObA":
                    		self.running=False
            	except: 
                	pass                         


		if self.Pos[0] == 0:
			print("Decke getroffen!")
			self.Color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
			if self.Dir ==0:
				self.Dir = 1
			if self.Dir ==2:
				self.Dir = 3
		if self.Pos[0] == 19:
			print("Boden getroffen!")
			self.Color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
			if self.Dir ==1:
				self.Dir = 0
			if self.Dir ==3:
				self.Dir = 2
		if self.Pos[1] == 0:
			print("Linke Wand getroffen!")
			self.Color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
			if self.Dir ==2:
				self.Dir = 0
			if self.Dir ==3:
				self.Dir = 1
		if self.Pos[1] == 9:
			print("Rechte Wand getroffen!")
			self.Color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
			if self.Dir ==0:
				self.Dir = 2
			if self.Dir ==1:
				self.Dir = 3
	 
		if self.Dir == 0:
			self.Pos[0] = self.Pos[0]-1
			self.Pos[1] = self.Pos[1]+1
		if self.Dir == 1:
			self.Pos[0] = self.Pos[0]+1
			self.Pos[1] = self.Pos[1]+1
		if self.Dir == 2:
			self.Pos[0] = self.Pos[0]-1
			self.Pos[1] = self.Pos[1]-1
		if self.Dir == 3:
			self.Pos[0] = self.Pos[0]+1
			self.Pos[1] = self.Pos[1]-1
	
		for x in range (0,20):
        		for y in range (0,10):
        			self.pixels[x][y]=[0,0,0]     
		self.pixels[self.Pos[0]][self.Pos[1]]=self.Color
		print self.Pos
		print self.Dir
            	self.draw()
            	time.sleep(0.05)
        print("Ball Animation closed")