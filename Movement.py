
# Helper class for players' movements
#
# The movements use an ease-in-out function that starts and ends slowly,
# reaching peak velocity at half-movement

class Movement:
    N, S, W, E = 1, 2, 4, 8
    DIRECTIONS = {
            N: lambda x, y, delta: (x, y - delta),
            E: lambda x, y, delta: (x + delta, y),
            S: lambda x, y, delta: (x, y + delta),
            W: lambda x, y, delta: (x - delta, y)
    }

    def isOutOfBounds(position, bounds):
        if position[0] < 0 or position[1] < 0:
            return True
        if position[0] > bounds[0] or position[1] > bounds[1]:
            return True
        return False
    
    def __init__(self, distance, direction, **kwargs):

        self._start = kwargs['startPos']
        self.direction = Movement.DIRECTIONS[direction]
        self._distance = distance
        self.timeDelta = kwargs.get('timeDelta', 0.03)
        self.onEnd = kwargs.get('end', lambda: None)
        self._bounce = kwargs.get('bounce', False)

        self._now = self._start
        self.time = 0 # 0 to 1, increasing by a rate of step
    
    def tick(self):
        self.time += self.timeDelta
        if self._bounce:
            self._now = self.direction(*self._start, self.easeInOutBounce() * self._distance)
        else:
            self._now = self.direction(*self._start, self.easeInOut() * self._distance)
        if self.time >= 1:
            self.onEnd()
        return self.now

    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, nstart):
        self.time = 0
        self._start = nstart
        self._now = self._start

    @property
    def now(self):
        return self._now

    @property
    def distance(self):
        return self._distance
    @distance.setter
    def distance(self, ndistance):
        self._distance = ndistance

    @property
    def bounce(self):
        return self._bounce
    @bounce.setter
    def bounce(self, b):
        self._bounce = b

    def endPosition(self):
        if not self._bounce:
            return self.direction(*self._start, self._distance)
        else:
            return self._start

    # https://math.stackexchange.com/questions/121720/ease-in-out-function/121755#121755
    def easeInOut(self):
        return Movement.parametricBlend(self.time, 3)

    def easeInOutBounce(self):
        twoTimes = self.time * 2
        if self.time <= 0.5:
            return Movement.parametricBlend(self.time, 3) * 2
        else:
            return (1 - Movement.parametricBlend(self.time, 3)) * 2

    def parametricBlend(x, alpha):
        return x**alpha / (x**alpha + (1 - x)**alpha)

    def __repr__(self):
        return '[Movement - distance: {}, start: {}, end: {}]'.format(self.distance, self._start, self.endPosition())
