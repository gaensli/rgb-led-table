#!/usr/bin/env python
import time
import colorsys
import pygame
import socket
from lib import xbox_read

PIXEL_SIZE = 3
gamma = bytearray(256)
pixels = [[[255 for x in range(3)] for x in range(12)] for x in range(24)]
brightness = 0.0
spidev = open("/dev/spidev0.0", "wb")


def draw():
    for row in pixels:
        for pixel in row:
            for color in pixel:
                c = int(color * brightness)
                spidev.write(chr(c & 0xFF))
    spidev.flush()
    time.sleep(0.001)


def showImage(img):
    global pixels
    pixels = img
    draw()


def turnOff():
    print("Turning all LEDs off")
    global pixels
    global brightness
    pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
    brightness = 1
    draw()


def fadeIn():
    print("Fading in...")
    global pixels
    global brightness
    brightness = 0
    while brightness < 1:
        draw()
        brightness += 0.05


def colorfade():
    global pixels
    h, s, v = 0.0, 1.0, 1.0
    while 1:
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        aktFarbe = [0.0 for x in range(3)]
        aktFarbe = round(r * 255, 0), round(g * 255, 0), round(b * 255, 0)
        pixels = [[aktFarbe for x in range(10)] for x in range(20)]
        draw()
        h = h + 0.005
        if (h > 1):
            h = h - 1.


def correct_pixel_brightness(pixel):
    corrected_pixel = bytearray(3)
    corrected_pixel[0] = int(pixel[0] / 1.1)
    corrected_pixel[1] = int(pixel[1] / 1.1)
    corrected_pixel[2] = int(pixel[2] / 1.3)

    return corrected_pixel


def filter_pixel(input_pixel, brightness):
    output_pixel = bytearray(PIXEL_SIZE)
    input_pixel[0] = int(brightness * input_pixel[0])
    input_pixel[1] = int(brightness * input_pixel[1])
    input_pixel[2] = int(brightness * input_pixel[2])

    output_pixel[0] = gamma[input_pixel[0]]
    output_pixel[1] = gamma[input_pixel[1]]
    output_pixel[2] = gamma[input_pixel[2]]
    return output_pixel


def simonSays():
    pygame.mixer.music.load("sounds/tetrisaccapella.ogg")
    # player = subprocess.Popen(["mplayer", "tetrisklavier.mp3", "loop 0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pygame.mixer.music.play(-1)
    global brightness
    global pixels
    sleeptime = 0.1
    brightness = 1.0
    simonOff()
    time.sleep(sleeptime)
    simonYellow('on')
    time.sleep(sleeptime)
    simonRed('on')
    time.sleep(sleeptime)
    simonGreen('on')
    time.sleep(sleeptime)
    simonBlue('on')
    time.sleep(sleeptime)
    simonYellow('off')
    time.sleep(sleeptime)
    simonRed('off')
    time.sleep(sleeptime)
    simonGreen('off')
    time.sleep(sleeptime)
    simonBlue('off')
    simonflash([0, 255, 0])


def simonOff():
    global pixels
    pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
    draw()


def simonYellow(mode):
    global pixels
    temp = [[5, 3], [5, 4], [5, 5], [5, 6], [6, 3], [6, 4], [6, 5], [6, 6], [7, 3], [7, 4], [7, 5], [7, 6], [8, 4],
            [8, 5]]
    if mode == 'on':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [255, 255, 0]
        klickSound = pygame.mixer.Sound("sounds/click.ogg")
        klickSound.play()
    elif mode == 'off':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [0, 0, 0]
    draw()


def simonRed(mode):
    global pixels
    temp = [[8, 7], [8, 8], [8, 9], [9, 0], [9, 1], [9, 2], [9, 3], [10, 6], [10, 7], [10, 8], [10, 9], [11, 0],
            [11, 1], [11, 2]]
    if mode == 'on':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [255, 0, 0]
    elif mode == 'off':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [0, 0, 0]
    draw()


def simonGreen(mode):
    global pixels
    temp = [[11, 4], [11, 5], [12, 3], [12, 4], [12, 5], [12, 6], [13, 3], [13, 4], [13, 5], [13, 6], [14, 3], [14, 4],
            [14, 5], [14, 6]]
    if mode == 'on':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [0, 255, 0]
    elif mode == 'off':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [0, 0, 0]
    draw()


def simonBlue(mode):
    global pixels
    temp = [[8, 0], [8, 1], [8, 2], [9, 6], [9, 7], [9, 8], [9, 9], [10, 0], [10, 1], [10, 2], [10, 3], [11, 7],
            [11, 8], [11, 9]]
    if mode == 'on':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [0, 0, 255]
    elif mode == 'off':
        for ind in temp:
            pixels[ind[0]][ind[1]] = [0, 0, 0]
    draw()


def herzSchlag(int):
    heart = [[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 0, 0]],
             [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 0, 0]],
             [[255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 255, 255]],
             [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 0, 0]],
             [[255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0],
              [255, 0, 0], [255, 0, 0], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
             [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
              [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]
    heartBeat = [[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 255, 255]],
                 [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 0, 0]],
                 [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 255, 255]],
                 [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 0, 0]],
                 [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 255, 255]],
                 [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 0, 0]],
                 [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0],
                  [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
                 [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255],
                  [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]
    for x in range(int):
        showImage(heart)
        time.sleep(0.3)
        showImage(heartBeat)
        time.sleep(1.5)


def simonflash(flashcolor):
    global pixels
    b = 0.0
    while b < 1.0:
        flash = [round(flashcolor[0] * b, 0), round(flashcolor[1] * b, 0), round(flashcolor[2] * b, 0)]
        pixels = [[flash for x in range(10)] for x in range(20)]
        draw()
        b = b + 0.1
        time.sleep(0.001)
    simonOff()


def pixelStream(UDP, PORT):
    print("Start Pixel listener " + UDP + ":" + str(PORT))
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP, PORT))
    UDP_BUFFER_SIZE = 600
    while True:
        data, addr = sock.recvfrom(UDP_BUFFER_SIZE)  # blocking call
        pixels_in_buffer = len(data) / PIXEL_SIZE  ##600bytes = 200 pixels
        pixels = bytearray(pixels_in_buffer * PIXEL_SIZE)  # Leeren Pixelbuffer erstellen
        for pixel_index in range(
                pixels_in_buffer):  # Jedes Pixel wird aus Datastream ausgelesen und ins Pixelarray ueberfuehrt
            pixel_to_adjust = bytearray(data[(pixel_index * PIXEL_SIZE):((pixel_index * PIXEL_SIZE) + PIXEL_SIZE)])
            pixel_to_filter = correct_pixel_brightness(pixel_to_adjust)  # Blauwerte daempfen
            pixels[((pixel_index) * PIXEL_SIZE):] = filter_pixel(pixel_to_filter[:], 1)  # Gamma-Koorektur anwenden

        spidev.write(pixels)
        spidev.flush()
        time.sleep(0.001)


if __name__ == '__main__':
    print("RGB-Tisch gestartet")
    for i in range(256):
        gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)
    print("Gamma-Korrektur vorgeladen")
    pygame.mixer.pre_init(11025, -16, 2, 4096)
    pygame.init()
    fadeIn()
    udpBild = [
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
         [255, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
         [255, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
         [255, 0, 0]],
        [[255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0],
         [255, 0, 0]],
        [[255, 0, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 0],
         [255, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    showImage(udpBild)
    time.sleep(1)
    simonSays()
    herzSchlag(200)
    pixelStream("192.168.1.49", 7766)

for event in xbox_read.event_stream(deadzone=12000):
    # if event.key=='RB' or event.key=='LB':
    #    if event.key=='RB' and event.value==1:
    #       if brightness < 1:
    #               brightness += 0.1
    #               print("Helligkeit um 10% erhoeht - Aktuell:",round(brightness*100,0),"%.")
    #               draw()
    #               time.sleep(0.1)
    #    elif event.key=='LB' and event.value==1:
    #       if brightness > .09:
    #               brightness -= 0.1
    #               print("Helligkeit um 10% erniedrigt - Aktuell:",round(brightness*100,0),"%.")
    #               draw()
    #               time.sleep(0.1)
    if event.key == 'RT':
        pixels = [[[255 for x in range(3)] for x in range(10)] for x in range(20)]
        brightness = round(1.0 * event.value / 255, 2)
        draw()
    if event.key == 'LT':
        colorfade()
    if event.key == 'A':
        if event.value == 1:
            simonGreen('on')
        else:
            simonGreen('off')
    if event.key == 'B':
        if event.value == 1:
            simonRed('on')
        else:
            simonRed('off')
    if event.key == 'X':
        if event.value == 1:
            simonBlue('on')
        else:
            simonBlue('off')
    if event.key == 'Y':
        if event.value == 1:
            simonYellow('on')
        else:
            simonYellow('off')
