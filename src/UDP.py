#!/usr/bin/env python
import time
import pygame
import socket

from src.Beat import RGB_Table, colorfade, heart_beat, RED, YELLOW, BLUE, GREEN, BLACK

PIXEL_SIZE = 3

class SimonSayGame:
    def __init__(self, display):
        self.display = display
        pass

    def simon_says(self):
        pygame.mixer.music.load("../sounds/tetrisaccapella.ogg")
        # player = subprocess.Popen(["mplayer", "tetrisklavier.mp3", "loop 0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pygame.mixer.music.play(-1)

        sleeptime = 1
        self.display.fill(BLACK)
        self.display.show()
        for color in ['yellow', 'red', 'green', 'blue']:
            self.simon_show_color(color, True)
            time.sleep(sleeptime)
        for color in ['yellow', 'red', 'green', 'blue']:
            self.simon_show_color(color, False)
            time.sleep(sleeptime)
        self.display.fill(BLACK)

    def simon_show_color(self, color: str, mode: bool):
        colors = {
            'red': RED,
            'green': GREEN,
            'blue': BLUE,
            'yellow': YELLOW
        }
        blocks = {
            'yellow': [[6, 4], [9, 7]],
            'red': [[10, 8], [13, 11]],
            'green': [[14, 4], [17, 7]],
            'blue': [[10, 0],[13, 3]],
        }

        if color in blocks and color in colors:
            block = blocks[color]
            fg_color = colors[color] if mode else BLACK
        else:
            return

        xy1, xy2 = block
        for x in range(xy1[0], xy2[0]+1):
            for y in range(xy1[1], xy2[1]+1):
                self.display.set_pixel(x, y, fg_color)
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
    pygame.joystick.init()
    clock = pygame.time.Clock()

    game = SimonSayGame(display)
    # game.simon_says()

    # heart_beat(display, 10)
    # pixelStream(display, "192.168.178.33", 7766)

    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("Error: Could not find any joysticks!")
        exit(1)

    j = pygame.joystick.Joystick(0)
    print(f"Initialized joystick: {j.get_name()}")

    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7: # 'RT'
                    display.fill([128, 128, 128])
                    display.brightness = 0.5 # round(1.0 * event.value / 255, 2)
                    display.show()

                if event.button == 6:   # 'LT'
                    colorfade(display)

            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                color = ""
                if event.button == 0:   # A
                    color = 'green'
                if event.button == 1: # B
                    color = 'red'
                if event.button == 3: # X
                    color = 'blue'
                if event.button == 4: # Y
                    color = 'yellow'

                if color:
                    game.simon_show_color(color, event.type == pygame.JOYBUTTONDOWN)
