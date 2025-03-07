import pygame

pygame.init()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

print(joysticks)

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            print(f"Joystick axis motion: {event}")
        
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Joystick button pressed: {event}")

        if event.type == pygame.JOYBUTTONUP:
            print(f"Joystick button released: {event}")
