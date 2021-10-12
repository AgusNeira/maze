import sys, pygame
from Player import Player

pygame.init()

size = width, height = 600, 400
speed = 2, 2
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

screen = pygame.display.set_mode(size)
screen.fill(black)

player = Player()
player.position = 7.5, 7.5
player.size = 15, 15
player.speed = 5
player.color = 0, 0, 0
player.boundaries = width, height
player.step = 5

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement = Player.NORTH
            elif event.key == pygame.K_DOWN:
                player.movement = Player.SOUTH
            elif event.key == pygame.K_LEFT:
                player.movement = Player.WEST
            elif event.key == pygame.K_RIGHT:
                player.movement = Player.EAST
        elif event.type == pygame.KEYUP:
            player.movement = None
    player.tick()

    screen.fill(black)
    player.draw(screen)

    pygame.display.flip()
    pygame.time.delay(20)

