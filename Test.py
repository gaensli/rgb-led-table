#!/usr/bin/env python
from datetime import datetime
import time
import colorsys

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
WIDTH = 24
HEIGHT = 12
PIXEL_COUNT = WIDTH * HEIGHT

PIXEL_MAPPING = []
for col in range(WIDTH):
    col_map = []
    for row in range(HEIGHT):
        if row % 2 == 0:
            col_map.append(row * 24 + col)
        else:
            col_map.append(((row + 1) * 24 - (col + 1)))
    PIXEL_MAPPING.append(col_map)

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def show_digit(position, digit, color):
    x_pos = [4, 8, 14, 18]
    y_pos = 4

    digit_to_pixel = {
        '0': [[1, 1, 1],
              [1, 0, 1],
              [1, 0, 1],
              [1, 0, 1],
              [1, 1, 1]],
        '1': [[0, 1, 1],
              [0, 0, 1],
              [0, 0, 1],
              [0, 0, 1],
              [0, 0, 1]],
        '2': [[1, 1, 1],
              [0, 0, 1],
              [1, 1, 1],
              [1, 0, 0],
              [1, 1, 1]],
        '3': [[1, 1, 1],
              [0, 0, 1],
              [0, 1, 1],
              [0, 0, 1],
              [1, 1, 1]],
        '4': [[1, 0, 1],
              [1, 0, 1],
              [1, 1, 1],
              [0, 0, 1],
              [0, 0, 1]],
        '5': [[1, 1, 1],
              [1, 0, 0],
              [1, 1, 1],
              [0, 0, 1],
              [1, 1, 1]],
        '6': [[1, 1, 1],
              [1, 0, 0],
              [1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]],
        '7': [[1, 1, 1],
              [0, 0, 1],
              [0, 0, 1],
              [0, 0, 1],
              [0, 0, 1]],
        '8': [[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]],
        '9': [[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1],
              [0, 0, 1],
              [1, 1, 1]],
    }

    d = digit_to_pixel[digit]
    for x in range(3):
        for y in range(5):
            if d[y][x]:
                pixels.set_pixel(PIXEL_MAPPING[x + x_pos[position]][y_pos + 4 - y], color)

def show_dots(color):
    pixels.set_pixel(PIXEL_MAPPING[12][5], color)
    pixels.set_pixel(PIXEL_MAPPING[12][7], color)

def time_display():
    print("time_display")

    fg_color = Adafruit_WS2801.RGB_to_color(255, 0, 0)
    bg_color = Adafruit_WS2801.RGB_to_color(0, 0, 0)
    while True:
        pixels.set_pixels(bg_color)

        now = time.localtime()
        timestring = time.strftime("%H%M%S", now)
        for pos, digit in enumerate(timestring[0:4]):
            show_digit(pos, digit, fg_color)

        seconds = now.tm_sec
        if seconds % 2 == 0:
            show_dots(fg_color)

        pixels.show()
        time.sleep(0.1)


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
    # fade_in_out()
    # color_chase()
    time_display()
