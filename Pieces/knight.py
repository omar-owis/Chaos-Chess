from ..helpers import *

from .piece import *


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.capture_directions = KNIGHT_DIRECTIONS
        self.extend_direction = False
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/white-knight.png"))\
            if color is WHITE else pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/black-knight.png"))

    def conditional_directions(self, **conditions):
        return []
