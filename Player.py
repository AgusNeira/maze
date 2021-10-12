import pygame

# A basic arrow controlled player, represented by a rectangle.
# Moves orthogonally

class Player:
    NORTH = lambda x, y, step: (x, y - step)
    EAST = lambda x, y, step: (x + step, y)
    SOUTH = lambda x, y, step: (x, y + step)
    WEST = lambda x, y, step: (x - step, y)

    def isOutOfBounds(pos, size, bounds):
        if bounds == None:
            return False
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[0] + size[0] > bounds[0]:
            return True
        if pos[1] + size[1] > bounds[1]:
            return True
        return False

    def __init__(self, **kwargs):
        self.x, self.y = kwargs.get("position", (0, 0))
        self.width, self.height = kwargs.get("size", (10, 10))
        self._speed = kwargs.get("speed", 5)
        self._color = kwargs.get("color", pygame.Color(255, 255, 255))
        self._boundaries = kwargs.get("boundaries", None)
        self._step = kwargs.get('step', 10)

        self._movement = None

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)


    def tick(self):
        if self.movement:
            self.position = self.movement(*self.position, self.step)

    def draw(self, surface):
        surface.blit(self.surface, self.position)

    @property
    def position(self):
        return self.x, self.y
    @position.setter
    def position(self, nx, ny):
        if not Player.isOutOfBounds((nx, ny), self.size, self.boundaries):
            self.x, self.y = nx, ny
        else:
            raise ValueError("New position out of bounds")
    @position.setter
    def position(self, npos):
        if not Player.isOutOfBounds(npos, self.size, self.boundaries):
            self.x, self.y = npos
        else:
            raise ValueError("New position out of bounds")

    @property
    def size(self):
        return self.width, self.height
    @size.setter
    def size(self, nwidth, nheight):
        if not Player.isOutOfBounds(self.position, (nwidth, nheight), self.boundaries):
            self.width, self.height = nwidth, nheight
            del self.surface
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(self.color)
        else:
            raise ValueError("New size set Player out of bounds")
    @size.setter
    def size(self, nsize):
        if not Player.isOutOfBounds(self.position, nsize, self.boundaries):
            self.width, self.height = nsize
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
        elif type(ncolor) == 'tuple':
            self._color = pygame.Color(*rgb)
            self.surface.fill(self.color)

    @property
    def boundaries(self):
        return self._boundaries
    @boundaries.setter
    def boundaries(self, nboundaries):
        if not Player.isOutOfBounds(self.position, self.size, self.boundaries):
            self._boundaries = nboundaries
        else:
            raise ValueError("New boundaries must contain the Player")

    @property
    def step(self):
        return self._step
    @step.setter
    def step(self, nstep):
        self._step = nstep

    @property
    def movement(self):
        return self._movement
    @movement.setter
    def movement(self, nmove):
        self._movement = nmove
