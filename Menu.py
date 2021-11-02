import pygame
from FontPool import FontPool

class Menu:
    def __init__(self, size, title, options):
        self.size = size
        pygame.font.init()

        self.surface = pygame.Surface(self.size)

        bigFont = FontPool.get(32)
        font = FontPool.get(18)

        titles = title.split('\n')

        self.titles = [bigFont.render(ti, False, pygame.Color(255, 255, 255)) for ti in titles]
        self.titlePos = [(self.centerHorizontally(ti), self.size[1] // 4 + 40 * i) for i, ti in enumerate(self.titles)]

        self.menuOptions = options
        self.initOptions(font, self.size[1] * 2.5 // 4, 24)
        self.currOption = 0

        self.cursor = {
                'surface': font.render('~', False, pygame.Color(255, 255, 255))
        }
        self.updateCursorPosition()
        
    
    def initOptions(self, font, startHeight, lineHeight):
        for index, option in enumerate(self.menuOptions):
            option['surface'] = font.render(option['name'], False, pygame.Color(255, 255, 255))
            option['position'] = self.centerHorizontally(option['surface']), startHeight + lineHeight * index

    def draw(self, surface):
        self.surface.fill(pygame.Color(0, 0, 0))
        [self.surface.blit(ti, pos) for ti, pos in zip(self.titles, self.titlePos)]
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
