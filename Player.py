import pygame

# A basic arrow controlled player, represented by a rectangle.

class Player:
    def __init__(self, **kwargs):
        self.x, self.y = kwargs.get("position", (0, 0))
        self.width, self.height = kwargs.get("size", (10, 10))
        self.speed = kwargs.get("speed", [5, 5])
        self._color = kwargs.get("color", pygame.Color(255, 255, 255))
        self._boundaries = kwargs.get("boundaries", None)

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)

    @property
    def position(self):
        return self.x, self.y
    @position.setter
    def position(self, nx, ny):
        if self.boundaries is None or (nx + self.witdh <= self.boundaries[0] and ny + self.height <= self.boundaries[1]):
            self.x, self.y = nx, ny
        else:
            raise ValueError("New position out of bounds")
    @position.setter
    def position(self, npos):
        if self.boundaries is None or (npos[0] + self.width <= self.boundaries[0] and npos[1] + self.height <= self.boundaries[1]):
            self.x, self.y = npos
        else:
            raise ValueError("New position out of bounds")

    @property
    def size(self):
        return self.width, self.height
    @size.setter
    def size(self, nwidth, nheight):
        if self.boundaries and self.x + nwidth <= self.boundaries[0] and self.y + nheight <= self.boundaries[1]:
            self.width, self.height = nwidth, nheight
            del self.surface
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(self.color)
        else:
            raise ValueError("New size set Player out of bounds")

    @property
    def speed(self):
        return self._speed
    @speed.setter
    def speed(self, nspeed):
        self._speed = nspeed

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, ncolor):
        if isinstance(ncolor, pygame.Color):
            self._color = ncolor
            self.surface.fill(self.color)

    @property
    def boundaries(self):
        return self._boundaries
    @boundaries.setter
    def boundaries(self, nboundaries):
        if self.x + self.width <= nboundaries[0] and self.y + self.height <= nboundaries[1]:
            self._boundaries = nboundaries
        else:
            raise ValueError("New boundaries must contain the Player")

    def tick(self):
        self.position = [pos + speed for (pos, speed) in zip(self.position, self.speed)]

    def draw(self, surface):
        surface.blit(self.surface, self.position)

