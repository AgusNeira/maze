import pygame, random, sys
from functools import reduce
from Player import Player
from FontPool import FontPool

class Maze:
    N, S, W, E = 1, 2, 4, 8
    DX = { N: 0, S: 0, W: -1, E: 1 }
    DY = { N: -1, S: 1, W: 0, E: 0 }
    OPPOSITE = { N: S, S: N, W: E, E: W }

    def __init__(self, cols, rows, size):
        self.name = 'maze'
        # Adjust maze size to fit all the square cells, with a 10px margin
        # and 30px on top to hold movement counter
        if size[0] / cols > (size[1] - 30) / rows:
            self.cellSize = (size[1] - 50) / rows
            self.position = (size[0] - self.cellSize * cols) / 2, 40
        else:
            self.cellSize = (size[0] - 20) / cols
            self.position = 10, (size[1] - self.cellSize * rows) / 2 + 30

        self.size = [self.cellSize * cells for cells in [cols, rows]]
        self.rows = rows
        self.cols = cols

        # The grid holds information about which passages are free
        # Coded in 4 bits (1, 2, 4, 8 for N, S, W, E)
        # Meaning the presence of the bit indicates the absence of the wall,
        # and viceversa
        self._grid = [[0 for _ in range(rows)] for _ in range(cols)]
        self.generate()

        self._surface = pygame.Surface(size)
        self._surface.fill(pygame.Color(0, 0, 0))

        self.draw_walls()

        playerSize = [self.cellSize / 2] * 2
        playerOffset = [self.cellSize / 4] * 2
        self.player = Player(size = playerSize, step = self.cellSize)
        self.player.position = [pos + off for pos, off in zip(self.position, playerOffset)]
        self.player.speed = 10
        self.player.color = 0, 0, 0

        self.moves = 0
        self.updateMovesCounter()

    def generate(self):
        def choose_index(ceil):
            # 50/50 algorithm, varies between recursive backtracker and Prim's algorithm (random)
            if random.choice([True, False]):
                return ceil - 1
            else: 
                return random.randrange(ceil)

        # Select a random cell to start from
        cells = [(random.randrange(self.cols), random.randrange(self.rows))]
        print(cells)

        while len(cells) > 0:
            curr_cell = choose_index(len(cells))
            x, y = cells[curr_cell]

            for direction in random.sample([Maze.N, Maze.S, Maze.W, Maze.E], k=4):
                nx, ny = x + Maze.DX[direction], y + Maze.DY[direction]
                if nx >= 0 and nx < self.cols and ny >= 0 and ny < self.rows and self._grid[nx][ny] == 0:
                    self._grid[x][y] |= direction
                    self._grid[nx][ny] |= Maze.OPPOSITE[direction]
                    cells.append((nx, ny))

                    curr_cell = -1
                    break
            if curr_cell != -1:
                del cells[curr_cell]

    def isThereAWall(self, col, row, direction):
        return self._grid[col][row] & direction == 0

    def draw_walls(self):
        h_walls = []
        v_walls = []

        def group_h_walls(previous, curr):
            last = previous[-1]
            if last[0] + last[2] == curr[0] and last[1] == curr[1]:
                group = (last[0], last[1], last[2] + 1)
                return [*previous[:-1], group]
            else:
                return [*previous, curr]
        def group_v_walls(previous, curr):
            last = previous[-1]
            if last[0] == curr[0] and last[1] + last[2] == curr[1]:
                group = (last[0], last[1], last[2] + 1)
                return [*previous[:-1], group]
            else:
                return [*previous, curr]

        for y in range(self.rows):
            for x in range(self.cols):
                if y == 0 and self.isThereAWall(x, y, Maze.N):
                    h_walls.append((x, y, 1))
                if self.isThereAWall(x, y, Maze.S):
                    h_walls.append((x, y + 1, 1)) 

        for x in range(self.cols):
            for y in range(self.rows):
                if x == 0 and self.isThereAWall(x, y, Maze.W):
                    v_walls.append((x, y, 1))
                if self.isThereAWall(x, y, Maze.E):
                    v_walls.append((x + 1, y, 1))

        h_walls = reduce(group_h_walls, h_walls[1:], [h_walls[0]])
        v_walls = reduce(group_v_walls, v_walls[1:], [v_walls[0]])
        
        # Adding the winning square
        winSquareLeft = self.size[0] - self.cellSize
        winSquareTop = self.size[1] - self.cellSize
        winSquareRect = pygame.Rect(winSquareLeft, winSquareTop, self.cellSize, self.cellSize)
        pygame.draw.rect(self._surface, pygame.Color(255, 0, 0), winSquareRect)

        # Actual drawing
        cell_size = self.size[0] / self.cols, self.size[1] / self.rows
        wall_color = pygame.Color(255, 255, 255)
        for wall in h_walls:
            start_pos = wall[0] * self.cellSize, wall[1] * self.cellSize
            end_pos = (wall[0] + wall[2]) * self.cellSize, start_pos[1]
            pygame.draw.line(self._surface, wall_color, start_pos, end_pos)

        for wall in v_walls:
            start_pos = wall[0] * self.cellSize, wall[1] * self.cellSize
            end_pos = start_pos[0], (wall[1] + wall[2]) * self.cellSize
            pygame.draw.line(self._surface, wall_color, start_pos, end_pos)
        
    def tick(self):
        self.player.tick()
        if not self.player.isMoving() and self.goalReached(self.interpolateCellIndex(self.player.position)):
            return self.moves

    def draw(self, surface):
        surface.blit(self._surface, self.position)
        surface.blit(self.movesCounter, self.movesCounterPos)
        self.player.draw(surface)

    def listen(self, event):
        if event.type == pygame.KEYDOWN:
            col, row = self.interpolateCellIndex(self.player.finalPosition())
            if event.key == pygame.K_UP:
                self.player.enqueueMovement(Maze.N, halfStep = self.isThereAWall(col, row, Maze.N))
                self.moves += 1
            elif event.key == pygame.K_DOWN:
                self.player.enqueueMovement(Maze.S, halfStep = self.isThereAWall(col, row, Maze.S))
                self.moves += 1
            elif event.key == pygame.K_LEFT:
                self.player.enqueueMovement(Maze.W, halfStep = self.isThereAWall(col, row, Maze.W))
                self.moves += 1
            elif event.key == pygame.K_RIGHT:
                self.player.enqueueMovement(Maze.E, halfStep = self.isThereAWall(col, row, Maze.E))
                self.moves += 1
            self.updateMovesCounter()

    def interpolateCellIndex(self, pos):
        x, y = pos
        return int((x - self.position[0]) / self.cellSize), int((y - self.position[1]) / self.cellSize)

    def goalReached(self, pos):
        col, row = pos
        return col == self.cols - 1 and row == self.rows - 1

    def updateMovesCounter(self):
        self.movesCounter = FontPool.get(18)\
                .render('Moves: %d' % self.moves, False, pygame.Color(255, 255, 255))
        self.movesCounterPos = self.position[0] + self.size[0] - self.movesCounter.get_width() - 20, 6
