"""
Snake Game

Reference: www.cs1graphics.org
"""

import time
import random

from _cs1graphics import *

GAME_BOARD_WIDTH = 600
GAME_BOARD_HEIGHT = 300
GAME_BOARD_BACKGROUND_COLOR = "darkgrey"
GAME_BOARD_TITLE = "Snake Game, Point: 0"

TOTAL_POINT = 0
SNAKE_DIRECTION = 1 # Default to right
"""
Directions of the snake 
    -1: Left
     2: Down
     1: Right
    -2: Up
"""

class DirectionHandler(EventHandler):


    def handle(self, event):
        """Check and change skane direction according to pressed key."""
        if event.getDescription() == 'keyboard':
            directions = {'a': turn_left, 'd': turn_right,}
            pressed_key = event.getKey().lower()
            if pressed_key in directions:
                direction = directions[pressed_key]
                direction()
                

def get_next_coordinate():
    x = random.randint(16, GAME_BOARD_WIDTH - 16)
    y = random.randint(16, GAME_BOARD_HEIGHT - 16)
    return x, y

def sort_by_second(t):
    return t[1]

def get_snake_positions():
    snake_x, snake_y = snake.getReferencePoint().get()
    positions = [obj.getReferencePoint().get() for obj in snake.getContents()]
    positions.sort()
    min_x = snake_x + positions[0][0]
    max_x = snake_x + positions[-1][0]
    positions.sort(key=sort_by_second)
    min_y = snake_y + positions[0][1]
    max_y = snake_y + positions[-1][1]
    return min_x, min_y, max_x, max_y

def check_apple():
    """Change the position of the apple to a new XY coordinate."""
    min_x, min_y, max_x, max_y = get_snake_positions()
    apple_x, apple_y = apple.getReferencePoint().get()
    if (abs(apple_x - min_x) < 10 or abs(apple_x - max_x) < 10) and (abs(apple_y - min_y) < 10 or abs(apple_y - max_y) < 10):
        snake_x, snake_y = snake.getContents()[0].getReferencePoint().get()
        circle_point = Circle(3, Point(snake_x, snake_y))
        snake.add(circle_point)
        x, y = get_next_coordinate()
        apple.moveTo(x, y)
        global TOTAL_POINT
        TOTAL_POINT += 1
        game_board.setTitle("Snake Game, Point: " + str(TOTAL_POINT))
        time.sleep(0.05)

def check_boundery(direction):
    x, y = snake.getReferencePoint().get()
    if direction == 1 and GAME_BOARD_WIDTH == x:
        snake.moveTo(0, y)
    elif direction == -1 and x < 0:
        snake.moveTo(GAME_BOARD_WIDTH, y)
    elif direction == 2 and GAME_BOARD_HEIGHT == y:
        snake.moveTo(x, 0)
    elif direction == -2 and y < 0:
        snake.moveTo(x, GAME_BOARD_HEIGHT)

def run():
    dx = 0 if SNAKE_DIRECTION % 2 == 0 else SNAKE_DIRECTION / abs(SNAKE_DIRECTION)
    dy = 0 if SNAKE_DIRECTION % 2 == 1 else SNAKE_DIRECTION / abs(SNAKE_DIRECTION)
    snake.move(dx, dy)
    check_apple()
    check_boundery(SNAKE_DIRECTION)

def turn(dirc, next_option):
    head_x, head_y = snake.getContents()[-1].getReferencePoint().get()
    global SNAKE_DIRECTION
    for diff, body in enumerate(snake.getContents()):
        body_x, body_y = body.getReferencePoint().get()
        if SNAKE_DIRECTION % 2 != 0:
            body.moveTo(head_x, head_y + dirc * SNAKE_DIRECTION * (diff + 1) * 12)
        else:
            body.moveTo(head_x + ( -dirc * (SNAKE_DIRECTION / 2)) * (diff + 1) * 12, head_y)
        time.sleep(0.005)
    SNAKE_DIRECTION = next_option[SNAKE_DIRECTION]

def turn_right():
    next_option = {1: 2, 2: -1, -1: -2, -2: 1}
    turn(1, next_option)

def turn_left():
    next_option = {1: -2, -2: -1, -1: 2, 2: 1}
    turn(-1, next_option)


game_board = Canvas(w=GAME_BOARD_WIDTH, h=GAME_BOARD_HEIGHT, bgColor=GAME_BOARD_BACKGROUND_COLOR, title=GAME_BOARD_TITLE)

# Register event handler
direction_handler = DirectionHandler()
game_board.addHandler(direction_handler)

# Initialize snake
snake = Layer()
for point in (Point(16, 16), Point(28, 16), Point(40, 16)):
    circle_point = Circle(3, point)
    snake.add(circle_point)

game_board.add(snake) # Introduce snake into game board

# Apple that the snake will cosnume
initial_x, initial_y = get_next_coordinate()
apple = Circle(5, Point(initial_x, initial_y))
apple.setFillColor("red")
apple.setBorderWidth(0)

game_board.add(apple)

while True:
    run()
    time.sleep(0.05)