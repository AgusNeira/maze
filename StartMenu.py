import pygame

class StartMenu:
    PLAY, EXIT = 1, 2
    def __init__(self, size):
        self.size = size
        pygame.font.init()
        self.name = 'start'

        self.surface = pygame.Surface(self.size)
        bigFont = pygame.font.Font('./Early GameBoy.ttf', 32)
        font = pygame.font.Font('./Early GameBoy.ttf', 18)
        white = pygame.Color(255, 255, 255)

        self.title = bigFont.render('The Maze', False, white)
        self.titlePos = self.centerHorizontally(self.title), self.size[1] // 4

        self.menuOptions = [
                {'name': 'Play', 'code': 1},
                {'name': 'Exit', 'code': 2}
        ]
        self.initOptions(font, self.size[1] * 2.5 // 4, 24)
        self.currOption = 0

        self.cursor = {
                'surface': font.render('~', False, white)
        }
        self.updateCursorPosition()

    def initOptions(self, font, startHeight, lineHeight):
        for index, option in enumerate(self.menuOptions):
            option['surface'] = font.render(option['name'], False, pygame.Color(255, 255, 255))
            option['position'] = self.centerHorizontally(option['surface']), startHeight + lineHeight * index

    def draw(self, surface):
        self.surface.fill(pygame.Color(0, 0, 0))
        self.surface.blit(self.title, self.titlePos)
        for option in self.menuOptions:
            self.surface.blit(option['surface'], option['position'])
        self.surface.blit(self.cursor['surface'], self.cursor['position'])
        surface.blit(self.surface, (0,0))

    def listen(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.currOption = (self.currOption - 1) % len(self.menuOptions)
                self.updateCursorPosition()
            elif event.key == pygame.K_DOWN:
                self.currOption = (self.currOption + 1) % len(self.menuOptions)
                self.updateCursorPosition()
            elif event.key == pygame.K_RETURN:
                return self.menuOptions[self.currOption]['code']
        return 0

    def tick(self):
        pass

    def centerHorizontally(self, txtSurface):
        return (self.size[0] - txtSurface.get_width()) / 2

    def updateCursorPosition(self):
        x, y = self.menuOptions[self.currOption]['position']
        x -= 30
        self.cursor['position'] = x, y
