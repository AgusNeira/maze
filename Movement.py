# Helper class for players' movements
#
# The movements use an ease-in-out function that starts and ends slowly,
# reaching peak velocity at half-movement

class Movement:
    NORTH = lambda x, y, delta: (x, y - delta)
    EAST = lambda x, y, delta: (x + delta, y)
    SOUTH = lambda x, y, delta: (x, y + delta)
    WEST = lambda x, y, delta: (x - delta, y)
    
    def __init__(self, distance, direction, **kwargs):
        self.direction = direction
        self.distance = distance
        self.timeDelta = kwargs.get('timeDelta', 0.03)
        self.onEnd = kwargs.get('end', lambda: None)

        self._now = self.start

        self.time = 0 # 0 to 1, increasing by a rate of step

    def start(self, pos):
        self.start = pos

    def tick(self):
        self.time += self.timeDelta
        self._now = self.direction(*self.start, self.easeInOut() * self.distance)
        if self.time >= 1:
            self.onEnd()
        return self.now

    @property
    def now(self):
        return self._now

    def endPosition(self):
        return self.direction(*self.start, self.distance)

    # https://math.stackexchange.com/questions/121720/ease-in-out-function/121755#121755
    def easeInOut(self):
        return self.time**3 / (self.time**3 + (1 - self.time)**3)
        
