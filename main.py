import sys, pygame
from Player import Player
from Movement import Movement
from Maze import Maze
from StartMenu import StartMenu

pygame.init()

screenSize = width, height = 1280, 720
speed = 2, 2
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN | pygame.SCALED)
screen.fill(black)

scene = StartMenu(screenSize)

while 1:
    for event in pygame.event.get():
        code = scene.listen(event)
        if scene.name == 'start':
            if code == StartMenu.PLAY:
                scene = Maze(10, 10, screenSize)
            elif code == StartMenu.EXIT:
                sys.exit()
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()

    if scene.tick() == Maze.WIN:
        scene = StartMenu(screenSize)
    screen.fill(black)
    scene.draw(screen)

    pygame.display.flip()
    pygame.time.delay(10)

