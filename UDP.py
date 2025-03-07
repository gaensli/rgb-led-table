#!/usr/bin/env python
import time
import pygame
import socket
from lib import xbox_read

from src.Beat import RGB_Table, colorfade, fade_in, heart_beat, RED, YELLOW, BLUE, GREEN, BLACK

PIXEL_SIZE = 3

class SimonSayGame:
    def __init__(self, display):
        self.display = display
        pass

    def simon_says(self):
        pygame.mixer.music.load("sounds/tetrisaccapella.ogg")
        # player = subprocess.Popen(["mplayer", "tetrisklavier.mp3", "loop 0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pygame.mixer.music.play(-1)

        sleeptime = 0.5
        self.display.fill(BLACK)
        self.display.show()
        for color in ['yellow', 'red', 'green', 'blue']:
            self.simon_show_color(color, True)
            time.sleep(sleeptime)
            self.simon_show_color(color, False)
            time.sleep(sleeptime)

        fade_in(display, GREEN)
        self.display.fill(BLACK)

    def simon_show_color(self, color: str, mode: bool):
        colors = {
            'red': RED,
            'green': GREEN,
            'blue': BLUE,
            'yellow': YELLOW
        }
        blocks = {
            'yellow': [[5, 3], [5, 4], [5, 5], [5, 6],
                       [6, 3], [6, 4], [6, 5], [6, 6],
                       [7, 3], [7, 4], [7, 5], [7, 6],
                       [8, 3], [8, 4], [8, 5], [8, 6]],
            'blue': [[8, 0], [8, 1], [8, 2], [8, 3],
                     [9, 0], [9, 1], [9, 2], [9, 3],
                     [10, 0], [10, 1], [10, 2], [10, 3],
                     [11, 0], [11, 1], [11, 2], [11, 3]],
            'green': [[11, 3], [11, 4], [11, 5], [11, 6],
                      [12, 3], [12, 4], [12, 5], [12, 6],
                      [13, 3], [13, 4], [13, 5], [13, 6],
                      [14, 3], [14, 4], [14, 5], [14, 6]],
            'red': [[8, 7], [8, 8], [8, 9], [8, 10],
                    [9, 7], [9, 8], [9, 9], [9, 10],
                    [10, 7], [10, 8], [10, 9], [10, 10],
                    [11, 7], [11, 8], [11, 9], [11, 10]]
        }

        if color in blocks and color in colors:
            temp = blocks[color]
            fg_color = colors[color] if mode else BLACK
        else:
            return

        for ind in temp:
            self.display.set_pixel(ind[0], ind[1], fg_color)
        self.display.show()


def correct_pixel_brightness(pixel):
    corrected_pixel = bytearray(3)
    corrected_pixel[0] = int(pixel[0] / 1.1)
    corrected_pixel[1] = int(pixel[1] / 1.1)
    corrected_pixel[2] = int(pixel[2] / 1.3)

    return corrected_pixel


def filter_pixel(pixel, brightness):
    output_pixel = [0] * 3

    def gamma(value):
        return int(pow(value / 255.0, 2.5) * 255.0)

    for index in range(3):
        output_pixel[index] = int(brightness * pixel[index])
        output_pixel[index] = gamma(output_pixel[index])

    return output_pixel


def pixelStream(display, UDP, PORT):
    FG = RED
    BG = BLACK
    udpBild = [
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, FG, FG, FG, FG, FG, BG, BG, BG],
        [BG, BG, BG, BG, FG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, FG, FG, FG, FG, FG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, FG, FG, FG, FG, FG, BG, BG, BG],
        [BG, BG, BG, BG, FG, BG, BG, BG, FG, BG, BG, BG],
        [BG, BG, BG, BG, BG, FG, FG, FG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, FG, FG, FG, FG, FG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, FG, BG, FG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, FG, FG, FG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
        [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
    ]

    display.fill(BLACK)
    display.show_image(udpBild)
    time.sleep(2)

    print(f"Start Pixel listener {UDP}:{PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # socker for ip/udp
    sock.bind((UDP, PORT))
    udp_buffer_size = 600

    while True:
        data, _ = sock.recvfrom(udp_buffer_size)
        pixels_in_buffer = int(len(data) / PIXEL_SIZE)
        pixels = bytearray(pixels_in_buffer * PIXEL_SIZE)
        for pixel_index in range(pixels_in_buffer):
            pixel_to_adjust = bytearray(data[(pixel_index * PIXEL_SIZE):((pixel_index * PIXEL_SIZE) + PIXEL_SIZE)])
            pixel_to_filter = correct_pixel_brightness(pixel_to_adjust)
            pixels[(pixel_index * PIXEL_SIZE):] = filter_pixel(pixel_to_filter, 1)

        display.show()
        time.sleep(0.001)


if __name__ == '__main__':
    display = RGB_Table()

    pygame.mixer.pre_init(11025, -16, 2, 4096)
    pygame.init()

    game = SimonSayGame(display)
    game.simon_says()

    heart_beat(display, 10)
    pixelStream(display, "192.168.178.33", 7766)

    for event in xbox_read.event_stream(deadzone=12000):
        if event.key == 'RT':
            display.fill([255,255,255])
            display.brightness = round(1.0 * event.value / 255, 2)
            display.show()

        if event.key == 'LT':
            colorfade(display)

        color = ""
        if event.key == 'A':
            color = 'green'
        if event.key == 'B':
            color = 'red'
        if event.key == 'X':
            color = 'blue'
        if event.key == 'Y':
            color = 'yellow'

        if color and event.value == 1:
            game.simon_show_color(color, True)
        elif color and event.value == 0:
            game.simon_show_color('green', False)
