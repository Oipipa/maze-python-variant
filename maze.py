import random

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[{'N': True, 'S': True, 'E': True, 'W': True, 'visited': False} for _ in range(width)] for _ in range(height)]

    def generate(self, start_x=0, start_y=0):
        stack = [(start_x, start_y)]
        self.grid[start_y][start_x]['visited'] = True
        while stack:
            x, y = stack[-1]
            neighbors = []
            if y > 0 and not self.grid[y - 1][x]['visited']:
                neighbors.append(('N', x, y - 1))
            if y < self.height - 1 and not self.grid[y + 1][x]['visited']:
                neighbors.append(('S', x, y + 1))
            if x < self.width - 1 and not self.grid[y][x + 1]['visited']:
                neighbors.append(('E', x + 1, y))
            if x > 0 and not self.grid[y][x - 1]['visited']:
                neighbors.append(('W', x - 1, y))
            if neighbors:
                direction, nx, ny = random.choice(neighbors)
                self.grid[y][x][direction] = False
                if direction == 'N':
                    self.grid[ny][nx]['S'] = False
                if direction == 'S':
                    self.grid[ny][nx]['N'] = False
                if direction == 'E':
                    self.grid[ny][nx]['W'] = False
                if direction == 'W':
                    self.grid[ny][nx]['E'] = False
                self.grid[ny][nx]['visited'] = True
                stack.append((nx, ny))
            else:
                stack.pop()
