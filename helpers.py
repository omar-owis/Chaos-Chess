from .data_classes import Position

WHITE = (255,255,255)
BLACK = (0, 0, 0)
BROWN = (150,75,0)
PURPLE = (128,0,128)

UP = Position(1,0)
DOWN = Position(-1, 0)
RIGHT = Position(0,1)
LEFT = Position(0, -1)
UP_RIGHT = Position(1, 1)
UP_LEFT = Position(1, -1)
DOWN_RIGHT = Position(-1, 1)
DOWN_LEFT = Position(-1, -1)
ALL_DIRECTIONS = [UP, DOWN, RIGHT, LEFT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
KNIGHT_DIRECTIONS = [Position(2,1), Position(2,-1), Position(-2,1), Position(-2,-1),
                           Position(1,2), Position(-1,2), Position(1,-2), Position(-1, -2)]