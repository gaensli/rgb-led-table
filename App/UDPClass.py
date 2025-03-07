#!/usr/bin/python
import math, sys
import time
import socket

class UDPTable:
    PIXEL_SIZE = 3
    UDP_BUFFER_SIZE = 600
    spidev = file("/dev/spidev0.0", "wb")
    
    def __init__(self,s):
        self.pixels = [[[255 for x in range(3)] for x in range(10)] for x in range(20)]
        self.brightness = 1.0
        self.s = s    
        self.StreamIP = "192.168.1.49"
        self.StreamPort = 7766
        self.running = True
        self.gamma = bytearray(256)
    def draw(self):
            for row in self.pixels:
                    for pixel in row:
                            for color in pixel:
                                    c = int(color*self.brightness)
                                    self.spidev.write(chr(c & 0xFF))
            self.spidev.flush()
            time.sleep(0.001)
            
    def showImage(self,img):
            self.pixels = img
            self.draw()
    
    def correct_pixel_brightness(self,pixel):
        corrected_pixel = bytearray(3)
        corrected_pixel[0] = int(pixel[0] / 1.1)
        corrected_pixel[1] = int(pixel[1] / 1.1)
        corrected_pixel[2] = int(pixel[2] / 1.3)
        return corrected_pixel
    
    def filter_pixel(self,input_pixel):
        output_pixel = bytearray(self.PIXEL_SIZE)
        input_pixel[0] = int(self.brightness * input_pixel[0])
        input_pixel[1] = int(self.brightness * input_pixel[1])
        input_pixel[2] = int(self.brightness * input_pixel[2])
    
        output_pixel[0] = self.gamma[input_pixel[0]]
        output_pixel[1] = self.gamma[input_pixel[1]]
        output_pixel[2] = self.gamma[input_pixel[2]]
        return output_pixel 
                          
    def pixelStream(self): 
        print ("Start PixelStream listener " + self.StreamIP + ":" + str(self.StreamPort)) 
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print("Socket created")
        sock.bind((self.StreamIP, self.StreamPort)) 
        print("Socket bound")
        while self.running: 
            try:
                print(".")
                data = self.s.recv(1024)
		print(",")
                if data=="AbOrTTrObA":
                    self.running=False
                print("-")
            except: 
                pass             
            data, addr = sock.recvfrom(self.UDP_BUFFER_SIZE)  # blocking call 
            pixels_in_buffer = len(data) / self.PIXEL_SIZE  ##600bytes = 200 pixels
            self.pixels = bytearray(pixels_in_buffer * self.PIXEL_SIZE) #Leeren Pixelbuffer erstellen
            for pixel_index in range(pixels_in_buffer): #Jedes Pixel wird aus Datastream ausgelesen und ins Pixelarray ueberfuehrt
                pixel_to_adjust = bytearray(data[(pixel_index * self.PIXEL_SIZE):((pixel_index * self.PIXEL_SIZE) + self.PIXEL_SIZE)])
                pixel_to_filter = correct_pixel_brightness(pixel_to_adjust) #Blauwerte daempfen
                self.pixels[((pixel_index) * self.PIXEL_SIZE):] = filter_pixel(pixel_to_filter[:]) #Gamma-Koorektur anwenden
            
            self.spidev.write(self.pixels)
            self.spidev.flush() 
            time.sleep(0.001)
        sock.close()
        print("UDP Modus beendet")
            
    def UDPStart(self):
            print("UDP-Modus gestartet")
            for i in range(256):
                    self.gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)
            udpBild = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]], [[255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]], [[255, 0, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
            self.showImage(udpBild)
            time.sleep(1)
            self.pixelStream()