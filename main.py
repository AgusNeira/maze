import sys, pygame
from Player import Player
from Movement import Movement
from Maze import Maze
from StartMenu import StartMenu
from LevelMenu import LevelMenu
from WinScreen import WinScreen

pygame.init()

screenSize = width, height = 1280, 720
speed = 2, 2
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN | pygame.SCALED)
screen.fill(black)

scene = StartMenu(screenSize)
lastLevel = LevelMenu.L1

getMaze = {
    LevelMenu.L1: lambda sz: Maze(10, 10, sz),
    LevelMenu.L2: lambda sz: Maze(15, 10, sz),
    LevelMenu.L3: lambda sz: Maze(20, 20, sz),
    LevelMenu.L4: lambda sz: Maze(40, 25, sz),
    LevelMenu.L5: lambda sz: Maze(50, 30, sz)
}

while 1:
    for event in pygame.event.get():
        code = scene.listen(event)
        if scene.name == 'start':
            if code == StartMenu.PLAY:
                scene = LevelMenu(screenSize)
            elif code == StartMenu.EXIT:
                sys.exit()
        elif scene.name == 'level':
            if code != 0:
                scene = getMaze[code](screenSize)
                lastLevel = code
        elif scene.name == 'win':
            if code == WinScreen.REPLAY:
                scene = getMaze[lastLevel](screenSize)
            elif code == WinScreen.LEVELS:
                scene = LevelMenu(screenSize)
            elif code == WinScreen.MAIN:
                scene = StartMenu(screenSize)
            elif code == WinScreen.EXIT:
                sys.exit()

        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()

    if scene.tick() == Maze.WIN:
        scene = WinScreen(screenSize)
    screen.fill(black)
    scene.draw(screen)

    pygame.display.flip()
    pygame.time.delay(10)

