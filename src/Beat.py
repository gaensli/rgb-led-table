import time
import colorsys
import random

from lib.WS2801 import WS2801Pixels, RGB_to_color, color_to_RGB
import Adafruit_GPIO.SPI as SPI

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
CYAN = [0, 255, 255]
YELLOW = [255, 255, 0]
MAGENTA = [255, 0, 255]
GREY = [50, 50, 50]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]


class RGB_Table:
    def __init__(self):
        # Configure the count of pixels:
        self.width = 24
        self.height = 12

        self._pixel_mapping = []
        for col in range(self.width):
            col_map = []
            for row in range(self.height):
                if row % 2 == 0:
                    col_map.append(row * 24 + col)
                else:
                    col_map.append(((row + 1) * 24 - (col + 1)))
            self._pixel_mapping.append(col_map)

        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.pixels = WS2801Pixels(self.width * self.height, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

        self._brightness = 1.0
        self._wait_time = 1 / 30

        self.pixels.clear()  # Clear all the pixels to turn them off.
        self.pixels.show()  # Make sure to call show() after changing any pixels!

    def set_pixel(self, x, y, rgb):
        r, g, b = int(rgb[0] * self._brightness), int(rgb[1] * self._brightness), int(rgb[2] * self._brightness)
        self.pixels.set_pixel_rgb(self._pixel_mapping[x][y], r, g, b)

    def fill(self, rgb):
        self.pixels.set_pixels_rgb(rgb[0], rgb[1], rgb[2])

    def set_each_pixel(self, fun):
        for i in range(self.height * self.width):
            r, g, b = fun()
            self.pixels.set_pixel_rgb(i, r, g, b)

    def show(self):
        self.pixels.show()

    def show_image(self, img):
        for x, line in enumerate(img):
            for y, pixel in enumerate(line):
                self.set_pixel(x, y, pixel)
        self.show()

    def __len__(self):
        return self.width * self.height

    def wait(self):
        time.sleep(self._wait_time)

    @property
    def wait_time(self):
        return self._wait_time
    @wait_time.setter
    def wait_time(self, value):
        self._wait_time = value

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = min(max(0.0, value), 1.0)

def hsv2rgb(h: float, s: float, v: float) -> tuple[int, ...]:
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def rgb2hsv(r: int, g: int, b: int) -> tuple[float, ...]:
    return tuple(float(i) for i in colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0))


def random_color(mode: str) -> tuple[int, int, int]:
    if mode == 'blue':
        r, g, b = hsv2rgb(random.uniform(0.35, 0.5), 1.0, 1.0)
    elif mode == 'green':
        r, g, b = hsv2rgb(random.uniform(0.68, 0.72), 1.0, 1.0)
    elif mode == 'red':
        r, g, b = hsv2rgb(random.uniform(0.95, 0.99), 1.0, 1.0)
    elif mode == 'sat':
        r, g, b = hsv2rgb(random.random(), 1.0, 1.0)
    else:
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    return r, g, b


def change_pixels_random(display, mode):
    # fade out on all pixels first
    fade_out = True
    fade_out_expo = 0.98
    if fade_out:
        for i in range(len(display)):
            r, g, b = display.pixels.get_pixel_rgb(i)
            if fade_out_expo:
                r = int(r * fade_out_expo)
                g = int(g * fade_out_expo)
                b = int(b * fade_out_expo)
            else:
                r = max(0, r - 1)
                g = max(0, g - 1)
                b = max(0, b - 1)
            display.pixels.set_pixel_rgb(i, r, g, b)

    # set 1 random pixel to random color
    row = random.randint(0, 23)
    col = random.randint(0, 11)
    display.set_pixel(row, col, random_color(mode))
    display.show()
    display.wait()


def wheel(pos: int) -> int:
    # Define the wheel function to interpolate between different hues.
    if 0 < pos < 85:
        return RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif 85 <= pos < 170:
        pos -= 85
        return RGB_to_color(255 - pos * 3, 0, pos * 3)
    elif 170 <= pos < 255:
        pos -= 170
        return RGB_to_color(0, pos * 3, 255 - pos * 3)
    else:
        return RGB_to_color(0, 0, 0)


# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(display):
    for i in range(len(display)):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (that is the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        display.pixels.set_pixel(i, wheel((i * 256 // len(display) % 256)))
        display.show()
        display.wait()


def rainbow_cycle(display):
    for j in range(10):  # one cycle of all 256 colors in the wheel
        for i in range(len(display)):
            display.pixels.set_pixel(i, wheel(((i * 256 // len(display)) + j) % 256))
        display.show()
        display.wait()


def rainbow_colors(display):
    rainbow_cycle_steps = 256
    for j in range(rainbow_cycle_steps):  # one cycle of all 256 colors in the wheel
        display.pixels.set_pixels(wheel((rainbow_cycle_steps // len(display) + j) % rainbow_cycle_steps))
        display.show()
        display.wait()


def rgb_decrease(display, step=1):
    for j in range(int(256 // step)):
        for i in range(len(display)):
            r, g, b = display.pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            display.pixels.set_pixel_rgb(i, r, g, b)
        display.show()


def blink_color(display, color=(255, 0, 0)):
    display.pixels.clear()
    # blink two times, then wait
    for j in range(2):
        display.pixels.set_pixels_rgb(color[0], color[1], color[2])
        display.show()
        display.wait()
        display.pixels.clear()
        display.show()
        display.wait()


def appear_from_back(display, color=(255, 0, 0)):
    for i in range(display.pixels.count()):
        for j in reversed(range(i, display.pixels.count())):
            display.pixels.clear()
            # first set all pixels at the beginning
            for k in range(i):
                display.pixels.set_pixel_rgb(k, color[0], color[1], color[2])
            # set then the pixel at position j
            display.pixels.set_pixel_rgb(j, color[0], color[1], color[2])
            display.show()
            display.wait()


def show_digit(display, position, digit, color):
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
                display.set_pixel(x + x_pos[position], y_pos + 4 - y, color)


def show_dots(display, color):
    display.set_pixel(12, 5, color)
    display.set_pixel(12, 7, color)


def time_display(display):
    # digit pixe# 0  0  0  1  1  1  2  2  2  3  3  3  4  4  4  5  5  5  6  6  6  7  7  7  8  8  8  9  9  9
    numMatrix = [[0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],    # x == 1
                 [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],    # x == 2
                 [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],    # x == 3
                 [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],    # x == 4
                 [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],    # x == 5
                 [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],    # x == 6
                 [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],    # x == 7
                 [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0]]    # x == 8

    fg_color = RED
    # fg_color = (255, 0, 0)
    bg_color = BLACK

    # TODO random color for digits and dots.

    display.pixels.set_pixels_rgb(bg_color[0], bg_color[1], bg_color[2])

    now = time.localtime()
    timestring = time.strftime("%H%M%S", now)
    for pos, digit in enumerate(timestring[0:4]):
        show_digit(display, pos, digit, fg_color)

    seconds = now.tm_sec
    if seconds % 2 == 0:
        show_dots(display, fg_color)

    display.show()
    display.wait()


def fade_in(display, rgb=(255, 255, 255)):
    display.brightness = 0.0
    while display.brightness < 1:
        r = int(rgb[0] * display.brightness)
        g = int(rgb[1] * display.brightness)
        b = int(rgb[2] * display.brightness)
        display.pixels.set_pixels_rgb(r, g, b)
        display.show()
        display.wait()
        display.brightness += 0.01


def fade_out(display, rgb=(255, 255, 255)):
    display._brightness = 1.0

    while display.brightness > 0:
        r = int(rgb[0] * display.brightness)
        g = int(rgb[1] * display.brightness)
        b = int(rgb[2] * display.brightness)
        display.pixels.set_pixels_rgb(r, g, b)
        display.show()
        display.wait()
        display.brightness -= 0.01

    display.pixels.set_pixels_rgb(0, 0, 0)
    display.show()


def color_chase(display):
    h, s, v = 0.0, 1.0, 1.0
    for led in range(len(display)):
        r, g, b = hsv2rgb(h, s, v)
        display.pixels.set_pixel_rgb(led, r, g, b)
        display.show()

        h += 1.0 / len(display)
        h = h - 1.0 if h > 1 else h


def colorfade(display):
    h, s, v = 0.0, 1.0, 1.0
    while True:
        rgb = hsv2rgb(h, s, v)
        display.fill(rgb)
        display.show()

        h += 0.005
        h = h - 1.0 if h > 1 else h


def heart_beat(display, repetitions):
    BG = [0, 0, 0]
    FG = [255, 0, 0]

    heart1 = [[BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, FG, FG, FG, BG, BG, BG, BG, BG, BG],
              [BG, BG, FG, FG, FG, FG, FG, BG, BG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG],
              [BG, BG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG],
              [BG, BG, BG, FG, FG, FG, FG, FG, FG, FG, FG, BG],
              [BG, BG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG, BG],
              [BG, BG, FG, FG, FG, FG, FG, BG, BG, BG, BG, BG],
              [BG, BG, BG, FG, FG, FG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG]]

    heart2 = [[BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, FG, FG, FG, BG, BG, BG, BG, BG, BG],
              [BG, BG, FG, FG, FG, FG, FG, BG, BG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG],
              [BG, BG, FG, FG, FG, FG, FG, FG, FG, FG, FG, BG],
              [BG, BG, BG, FG, FG, FG, FG, FG, FG, FG, FG, BG],
              [BG, BG, FG, FG, FG, FG, FG, FG, FG, FG, FG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG],
              [BG, FG, FG, FG, FG, FG, FG, FG, BG, BG, BG, BG],
              [BG, BG, FG, FG, FG, FG, FG, BG, BG, BG, BG, BG],
              [BG, BG, BG, FG, FG, FG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG],
              [BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG, BG]]

    for x in range(repetitions):
        display.show_image(heart1)
        time.sleep(0.1)
        display.show_image(heart2)
        time.sleep(0.1)
        display.show_image(heart1)
        time.sleep(0.1)
        display.show_image(heart2)
        time.sleep(0.5)


if __name__ == "__main__":
    display = RGB_Table()
    
    # rainbow_cycle_successive(display)
    # rainbow_cycle(display)
    # rainbow_colors(display)
    # rgb_decrease(display)
    # color_chase(display)
    # fade_in(display)
    # fade_out(display)
    # appear_from_back(display)

    while True:
        change_pixels_random(display, "blue")
        # time_display(display)
        # blink_color(display, color=(255, 0, 0))
        # blink_color(display, color=(0, 255, 0))
        # blink_color(display, color=(0, 0, 255))
        # blink_color(display, color=(255, 255, 255))
