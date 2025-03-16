from maze import Maze
from snake import Snake, Food
from renderer import MazeRenderer

def main():
    width = 20
    height = 20
    maze = Maze(width, height)
    maze.generate()
    food = Food(maze)
    snake = Snake(maze, food)
    renderer = MazeRenderer(maze, snake, food, cell_size=20)
    renderer.run()

if __name__ == '__main__':
    main()
