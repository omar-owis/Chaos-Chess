from ..helpers import *

from .piece import *


class Blank(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/blank.png"))

    def conditional_directions(self, **conditions):
        return []
