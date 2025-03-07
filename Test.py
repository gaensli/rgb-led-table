#!/usr/bin/env python
import time
import colorsys

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 288

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


numMatrix = [[0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
             [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
             [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
             [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0]]


def timedisplay():
    print("timedisplay")
    global pixels
    global brightness
    global numMatrix
    brightness = 1
    pixels = [[[0 for x in range(3)] for x in range(10)] for x in range(20)]
    while 1:
        timestring = time.strftime("%H%M")
        zahleins = int(timestring[0])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahleins * 3) + (y - 1)] == 1:
                    pixels[y][9 - x] = [255, 0, 0]
                else:
                    pixels[y][9 - x] = [0, 0, 0]
        zahlzwei = int(timestring[1])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahlzwei * 3) + (y - 1)] == 1:
                    pixels[y + 4][9 - x] = [255, 0, 0]
                else:
                    pixels[y + 4][9 - x] = [0, 0, 0]
        zahldrei = int(timestring[2])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahldrei * 3) + (y - 1)] == 1:
                    pixels[y + 11][9 - x] = [255, 0, 0]
                else:
                    pixels[y + 11][9 - x] = [0, 0, 0]
        zahlvier = int(timestring[3])
        for x in range(1, 9):
            for y in range(1, 4):
                if numMatrix[(x - 1)][(zahlvier * 3) + (y - 1)] == 1:
                    pixels[y + 15][9 - x] = [255, 0, 0]
                else:
                    pixels[y + 15][9 - x] = [0, 0, 0]
            # Punkte
        timestring = time.strftime("%S")
        if int(timestring) % 2 == 0:
            pixels[9][2] = [255, 0, 0]
            pixels[10][2] = [255, 0, 0]
            pixels[9][3] = [255, 0, 0]
            pixels[10][3] = [255, 0, 0]

            pixels[9][6] = [255, 0, 0]
            pixels[10][6] = [255, 0, 0]
            pixels[9][7] = [255, 0, 0]
            pixels[10][7] = [255, 0, 0]
        else:
            pixels[9][2] = [0, 0, 0]
            pixels[10][2] = [0, 0, 0]
            pixels[9][3] = [0, 0, 0]
            pixels[10][3] = [0, 0, 0]

            pixels[9][6] = [0, 0, 0]
            pixels[10][6] = [0, 0, 0]
            pixels[9][7] = [0, 0, 0]
            pixels[10][7] = [0, 0, 0]
        # drawsnake()
        time.sleep(1)


def fade_in_out():
    print("fade_in_out")
    brightness = 0.0
    while brightness < 1:
        rgb = int(255 * brightness)
        pixels.set_pixels(Adafruit_WS2801.RGB_to_color(rgb, rgb, rgb))
        pixels.show()
        time.sleep(0.02)
        brightness += 0.01
    brightness = 1.0

    while brightness > 0:
        rgb = int(255 * brightness)
        pixels.set_pixels(Adafruit_WS2801.RGB_to_color(rgb, rgb, rgb))
        pixels.show()
        time.sleep(0.02)
        brightness -= 0.01

    pixels.set_pixels(Adafruit_WS2801.RGB_to_color(0, 0, 0))
    pixels.show()


def color_chase():
    print("color_chase")
    h, s, v = 0.0, 1.0, 1.0
    for led in range(pixels.count()):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b  = int(r * 255), int(g * 255), int(b * 255)
        pixels.set_pixel(led, Adafruit_WS2801.RGB_to_color(r, g, b))
        pixels.show()

        h += 1.0 / pixels.count()
        if h > 1:
            h = h - 1.0


if __name__ == '__main__':
    fade_in_out()
    color_chase()
    timedisplay()
