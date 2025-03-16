import random
from collections import deque

class Food:
    def __init__(self, maze, get_snake_head=None):
        self.maze = maze
        self.position = self.random_position()
        self.get_snake_head = get_snake_head or (lambda: None)
    
    def set_snake_getter(self, getter):
        self.get_snake_head = getter
    
    def random_position(self):
        x = random.randrange(self.maze.width)
        y = random.randrange(self.maze.height)
        return (x, y)
    
    def get_neighbors(self, pos):
        x, y = pos
        cell = self.maze.grid[y][x]
        neighbors = []
        if not cell['N'] and y > 0:
            neighbors.append((x, y-1))
        if not cell['S'] and y < self.maze.height-1:
            neighbors.append((x, y+1))
        if not cell['E'] and x < self.maze.width-1:
            neighbors.append((x+1, y))
        if not cell['W'] and x > 0:
            neighbors.append((x-1, y))
        return neighbors

    def compute_distance(self, start, goal):
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            current, dist = queue.popleft()
            if current == goal:
                return dist
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist+1))
        return float('inf')
    
    def flood_fill_area(self, start):
        visited = set()
        queue = deque([start])
        area = 0
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            area += 1
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
        return area

    def move(self):
        neighbors = self.get_neighbors(self.position)
        if neighbors:
            snake_head = self.get_snake_head()
            best_moves = []
            max_score = -float('inf')
            for move in neighbors:
                dist = self.compute_distance(move, snake_head) if snake_head is not None else 0
                area = self.flood_fill_area(move)
                score = area + 3 * dist
                if score > max_score:
                    max_score = score
                    best_moves = [move]
                elif score == max_score:
                    best_moves.append(move)
            self.position = random.choice(best_moves)

class Snake:
    def __init__(self, maze, food):
        self.maze = maze
        self.food = food
        self.body = [(0, 0)]
        self.grow_flag = False
    
    def neighbors(self, pos):
        x, y = pos
        cell = self.maze.grid[y][x]
        result = []
        if not cell['N'] and y > 0:
            result.append((x, y-1))
        if not cell['S'] and y < self.maze.height-1:
            result.append((x, y+1))
        if not cell['E'] and x < self.maze.width-1:
            result.append((x+1, y))
        if not cell['W'] and x > 0:
            result.append((x-1, y))
        return result
    
    def find_path(self):
        start = self.body[0]
        goal = self.food.position
        if start == goal:
            return []
        queue = deque([start])
        came_from = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for n in self.neighbors(current):
                if n not in came_from:
                    queue.append(n)
                    came_from[n] = current
        if goal not in came_from:
            return []
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
    
    def update(self):
        path = self.find_path()
        if path:
            next_pos = path[0]
            self.body.insert(0, next_pos)
            if next_pos == self.food.position:
                self.grow_flag = True
                self.food.position = self.food.random_position()
            if not self.grow_flag:
                self.body.pop()
            else:
                self.grow_flag = False
