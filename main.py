import sys, pygame

pygame.init()

size = width, height = 600, 400
speed = 2, 2
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

screen = pygame.display.set_mode(size)
screen.fill(white)

player = pygame.Surface((20, 20))
playerRect = pygame.Rect(0, 0, 20, 20)
player.fill(black)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    playerRect.move_ip(speed)

    screen.fill(white)
    screen.blit(player, playerRect)

    pygame.display.flip()
    pygame.time.delay(20)

