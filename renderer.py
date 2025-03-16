import pygame
from maze import Maze
from snake import Snake, Food

class MazeRenderer:
    def __init__(self, maze, snake, food, cell_size=20, wall_color=(255,255,255), bg_color=(0,0,0), snake_color=(0,255,0), food_color=(255,0,0)):
        self.maze = maze
        self.snake = snake
        self.food = food
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.bg_color = bg_color
        self.snake_color = snake_color
        self.food_color = food_color
        self.width = maze.width * cell_size
        self.height = maze.height * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Snake")
        self.clock = pygame.time.Clock()

    def draw_maze(self):
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                if cell['N']:
                    pygame.draw.line(self.screen, self.wall_color, (x1, y1), (x1+self.cell_size, y1))
                if cell['S']:
                    pygame.draw.line(self.screen, self.wall_color, (x1, y1+self.cell_size), (x1+self.cell_size, y1+self.cell_size))
                if cell['W']:
                    pygame.draw.line(self.screen, self.wall_color, (x1, y1), (x1, y1+self.cell_size))
                if cell['E']:
                    pygame.draw.line(self.screen, self.wall_color, (x1+self.cell_size, y1), (x1+self.cell_size, y1+self.cell_size))

    def draw_snake(self):
        for pos in self.snake.body:
            x, y = pos
            rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.snake_color, rect)

    def draw_food(self):
        x, y = self.food.position
        rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, self.food_color, rect)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.draw_maze()
        self.draw_food()
        self.draw_snake()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.food.move()
            self.snake.update()
            self.draw()
            self.clock.tick(10)
        pygame.quit()
