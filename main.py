import sys, pygame
from Player import Player
from Movement import Movement
from Maze import Maze

pygame.init()

screenSize = width, height = 600, 400
speed = 2, 2
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

screen = pygame.display.set_mode(screenSize)
screen.fill(black)

maze = Maze(10, 10, screenSize)

while 1:
    for event in pygame.event.get():
        maze.listen(event)
        if event.type == pygame.QUIT: sys.exit()
        '''elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.enqueueMovement(Movement.NORTH)
            elif event.key == pygame.K_DOWN:
                player.enqueueMovement(Movement.SOUTH)            
            elif event.key == pygame.K_LEFT:
                player.enqueueMovement(Movement.WEST)
            elif event.key == pygame.K_RIGHT:
                player.enqueueMovement(Movement.EAST)
        elif event.type == pygame.KEYUP:
            player.movement = None'''

    maze.tick()
    screen.fill(black)
    maze.draw(screen)

    pygame.display.flip()
    pygame.time.delay(10)

