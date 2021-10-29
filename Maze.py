import pygame, random
from functools import reduce

class Maze:
    N, S, W, E = 1, 2, 4, 8
    DX = { N: 0, S: 0, W: -1, E: 1 }
    DY = { N: -1, S: 1, W: 0, E: 0 }
    OPPOSITE = { N: S, S: N, W: E, E: W }

    def __init__(self, rows, cols, size):
        self._size = size
        self._rows = rows
        self._cols = cols

        self._grid = [[0 for _ in range(rows)] for _ in range(cols)]
        self.generate()

        self._surface = pygame.Surface(size)
        self._surface.fill(pygame.Color(0, 0, 0))

        self.draw_walls()

    def generate(self):
        def choose_index(ceil):
            # 50/50 algorithm, varies between recursive backtracker and Prim's algorithm (random)
            '''if random.choice([True, False]):
                return ceil - 1
            else: 
                return random.randrange(ceil)
'''
            return ceil-1

        # Select a random cell to start from
        cells = [(0, 0)]

        while len(cells) > 0:
            curr_cell = choose_index(len(cells))
            x, y = cells[curr_cell]

            for direction in random.sample([Maze.N, Maze.S, Maze.W, Maze.E], k=4):
                nx, ny = x + Maze.DX[direction], y + Maze.DY[direction]
                if nx >= 0 and nx < self._cols and ny >= 0 and ny < self._rows and self._grid[nx][ny] == 0:
                    self._grid[x][y] |= direction
                    self._grid[nx][ny] |= Maze.OPPOSITE[direction]
                    cells.append((nx, ny))

                    curr_cell = -1
                    break
            if curr_cell != -1:
                del cells[curr_cell]
        print(self._grid)

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

        for y in range(self._rows):
            for x in range(self._cols):
                if self._grid[x][y] & Maze.S == 0:
                    h_walls.append((x, y, 1)) 

        for x in range(self._cols):
            for y in range(self._rows):
                if self._grid[x][y] & Maze.E == 0:
                    v_walls.append((x, y, 1))

        h_walls = reduce(group_h_walls, h_walls[1:], [h_walls[0]])
        v_walls = reduce(group_v_walls, v_walls[1:], [v_walls[0]])
        print(h_walls)
        print(v_walls)
        # Actual drawing
        cell_size = self._size[0] / self._cols, self._size[1] / self._rows
        wall_color = pygame.Color(255, 255, 255)
        for wall in h_walls:
            start_pos = wall[0] * cell_size[0], (wall[1] + 1) * cell_size[1]
            end_pos = (wall[0] + wall[2]) * cell_size[0], start_pos[1]
            pygame.draw.line(self._surface, wall_color, start_pos, end_pos)

        for wall in v_walls:
            start_pos = (wall[0] + 1) * cell_size[0], wall[1] * cell_size[1]
            end_pos = start_pos[0], (wall[1] + wall[2]) * cell_size[1]
            pygame.draw.line(self._surface, wall_color, start_pos, end_pos)

    def draw(self, surface):
        surface.blit(self._surface, (0, 0))
