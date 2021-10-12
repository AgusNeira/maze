import sys, pygame
from Player import Player

pygame.init()

size = width, height = 600, 400
speed = 2, 2
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

screen = pygame.display.set_mode(size)
screen.fill(black)

player = Player(size=(20, 20), speed=(2, 2), color=white)
player.boundaries = width, height

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    player.tick()

    screen.fill(black)
    player.draw(screen)

    pygame.display.flip()
    pygame.time.delay(20)

