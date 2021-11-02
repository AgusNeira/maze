import pygame

class FontPool:
    src = './Early GameBoy.ttf'
    pool = {}

    def get(size):
        if size not in FontPool.pool:
            FontPool.pool[size] = pygame.font.Font(FontPool.src, size)
        return FontPool.pool[size]

