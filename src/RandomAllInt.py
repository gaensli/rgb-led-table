from random import shuffle

import pygame

from src.Beat import RGB_Table, change_pixels_random


def next_mode():
    modes = ["red", "green", "blue", "sat"]
    shuffle(modes)
    return modes[0]

if __name__ == '__main__':
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("Error: Could not find any joysticks!")
        exit(1)

    j = pygame.joystick.Joystick(0)
    print(f"Initialized joystick: {j.get_name()}")

    display = RGB_Table()
    mode = next_mode()

    brightness_step = 0.01
    wait_time_step = 0.02

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                print(f"Joystick axis motion: {event}")

                if j.get_axis(1) <= -0.5:
                    display.brightness += brightness_step

                if j.get_axis(1) >= +0.5:
                    display.brightness -= brightness_step

                if j.get_axis(0) >= +0.5:
                    display.wait_time = min(1.0, display.wait_time + wait_time_step)

                if j.get_axis(0) <= -0.5:
                    display.wait_time = max(0.0, display.wait_time - wait_time_step)

                print(f'brightness: {display.brightness:3.2f}')
                print(f'wait_time: {display.wait_time:3.2f}')

            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick button pressed: {event}")

                if j.get_button(0):  # Button A - right red button - Rotate right
                    lastPressed = "A"
                if j.get_button(1):  # Button B - left red button - Rotate left
                    lastPressed = "B"
                if j.get_button(3):
                    lastPressed = "X"
                if j.get_button(4):
                    lastPressed = "Y"
                if j.get_button(6):
                    lastPressed = "L"
                if j.get_button(7):
                    lastPressed = "R"
                if j.get_button(10):
                    lastPressed = "SELECT"
                    mode = next_mode()
                if j.get_button(11):
                    lastPressed = "START"

            if event.type == pygame.JOYBUTTONUP:
                print(f"Joystick button released: {event}")

        change_pixels_random(display, mode=mode)
        # clock.tick(25)