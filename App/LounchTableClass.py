import math, sys, time, random, colorsys, pygame, socket
from pygame.locals import *
from colorsys import hsv_to_rgb, rgb_to_hsv
class LoungeTable:
    REFRESHSCREEN = USEREVENT+1
    spidev = file("/dev/spidev0.0", "wb")
    
    def __init__(self,s,fromColor="000",toColor="000",brightness="1000",waittime="50"):
        self.fromcolor = float(float(fromColor)/360)
        self.tocolor = float(float(toColor)/360)
        self.pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
        self.brightness = float(brightness)/1000
        self.waittime = int(waittime)
        self.waitbright = 200
        self.waitint = 100
        self.running = True
        self.s = s
    def hsv2rgb(self,h,s,v):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    def rgb2hsv(self,r,g,b):
        return tuple(i  for i in colorsys.rgb_to_hsv(r/ 255.0, g/ 255.0, b/ 255.0))
    def draw(self):
            for row in self.pixels:
                    for pixel in row:
                            for color in pixel:
                                    c = int(color*self.brightness)
                                    self.spidev.write(chr(c & 0xFF))
            self.spidev.flush()
            time.sleep(0.001)
    def initScreen(self):
        for row in range(0,20):
            for pixel in range(0,10):
                r, g, b = self.hsv2rgb(random.uniform(self.fromcolor,self.tocolor),1,1)
                self.pixels[row][pixel]=[r,g,b]
        self.draw()
    def changePixels(self):
        for i in range(0,5):
            row = random.randint(0,19)
            col = random.randint(0,9)
            r, g, b = self.hsv2rgb(random.uniform(self.fromcolor,self.tocolor),1,1)
            self.pixels[row][col] = [r,g,b]
        self.draw()
    def startTable(self): 
        pygame.quit()
        print("LoungeTable started")
        pygame.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print ("Error, I did not find any joysticks")
        else:
            j = pygame.joystick.Joystick(0)
            j.quit()
            j.init()
            print 'Initialized Joystick : %s' % j.get_name()
        self.initScreen()
        pygame.time.set_timer(self.REFRESHSCREEN, self.waittime)
        cl = pygame.time.Clock()
        start = pygame.time.get_ticks()
        startbright = start
        startint = start
        while self.running:
            try:
                data = self.s.recv(1024)

                if data.startswith("LOU"):
                    self.fromcolor = float(float(data[3:6])/360)
                    self.tocolor = float(float(data[6:9])/360)
                    self.brightness = float(data[9:13])/1000
                    self.waittime = int(data[13:])
                    print("Parameters updated")
                elif data=="AbOrTTrObA":
                    self.running=False
            except: 
                pass
            pygame.event.pump()
            #Check if waitbright-Intervall has passed since last change of brightness and update if buttons pressed
            if (pygame.time.get_ticks()>=startbright+self.waitbright):
                if j.get_axis(1) <= -0.5:
                    if self.brightness <= 0.95:
                        self.brightness +=0.05
                        
                if j.get_axis(1) >= +0.5:
                    if self.brightness >= 0.05:
                        self.brightness -=0.05
                self.draw()
                startbright = pygame.time.get_ticks()
                            
            if (pygame.time.get_ticks()>=startint+self.waitint):
                if j.get_axis(0) >= +0.5:
                    if self.waittime <= 9980:
                        self.waittime +=20
                       
                if j.get_axis(0) <= -0.5:
                    if self.waittime >= 20:
                        self.waittime -=20
                startint = pygame.time.get_ticks() 
    
            if j.get_button(1):
                self.waittime = 1
                self.brightness = 1.0
                startint = pygame.time.get_ticks()
                self.changePixels()        
            
            if (pygame.time.get_ticks()>=start+self.waittime):
                self.changePixels()
                start = pygame.time.get_ticks()
        pygame.quit()
        print("LoungeTable closed")