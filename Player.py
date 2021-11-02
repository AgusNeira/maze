import pygame
from Movement import Movement

# A basic arrow controlled player, represented by a rectangle.
# Moves orthogonally

class Player:

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
        self.width, self.height = kwargs["size"]
        self._speed = kwargs.get("speed", 5)
        self._color = kwargs.get("color", pygame.Color(255, 255, 255))
        self._boundaries = kwargs.get("boundaries", None)
        self._step = kwargs['step']
        self._halfStep = kwargs.get('halfStep', self._step / 4)

        self.moves_queue = []

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)


    def tick(self):
        if len(self.moves_queue) > 0:
            self.position = self.moves_queue[0].tick()

    def draw(self, surface):
        surface.blit(self.surface, self.position)

    def enqueueMovement(self, direction, halfStep = False):
        nmovement = Movement(self._step if not halfStep else self._halfStep,
                    direction, 
                    end = self.dequeueMovement,
                    startPos = self.finalPosition(),
                    bounce = halfStep)

        self.moves_queue.append(nmovement)

    def dequeueMovement(self):
        del self.moves_queue[0]

    def finalPosition(self):
        if len(self.moves_queue) > 0:
            return self.moves_queue[-1].endPosition()
        else:
            return self.position

    def isMoving(self):
        return len(self.moves_queue) == 0

    @property
    def size(self):
        return self.width, self.height

    @property
    def position(self):
        return self.x, self.y
    @position.setter
    def position(self, nx, ny):
        if not Player.isOutOfBounds((nx, ny), self.size, self.boundaries):
            self.x, self.y = nx, ny
        else:
            raise ValueError(f'New position out of bounds: {nx} {ny}')
    @position.setter
    def position(self, npos):
        if not Player.isOutOfBounds(npos, self.size, self.boundaries):
            self.x, self.y = npos
        else:
            raise ValueError("New position out of bounds")

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
