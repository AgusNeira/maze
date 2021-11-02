import sys, pygame
from Player import Player
from Movement import Movement
from Maze import Maze
from StartMenu import StartMenu
from LevelMenu import LevelMenu

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
                scene = LevelMenu(screenSize)
            elif code == StartMenu.EXIT:
                sys.exit()
        elif scene.name == 'level':
            if code == LevelMenu.L1:
                scene = Maze(10, 10, screenSize)
            elif code == LevelMenu.L2:
                scene = Maze(15, 10, screenSize)
            elif code == LevelMenu.L3:
                scene = Maze(20, 20, screenSize)
            elif code == LevelMenu.L4:
                scene = Maze(40, 25, screenSize)
            elif code == LevelMenu.L5:
                scene = Maze(50, 30, screenSize)

        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()

    if scene.tick() == Maze.WIN:
        scene = StartMenu(screenSize)
    screen.fill(black)
    scene.draw(screen)

    pygame.display.flip()
    pygame.time.delay(10)

