from ..helpers import *

from .piece import *


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.moved = False
        self.capture_directions = [LEFT, RIGHT, UP, DOWN, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
        self.extend_direction = False
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/white-king.png"))\
            if color is WHITE else pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/black-king.png"))

    def conditional_directions(self, **conditions):
        """
        conditions handled by king: long_castle (bool), short_castle (bool), has_moved (bool), direction_list (list[bool])
        long_castle is set to true when: left path is clear for castling, left rook has not moved, path not blocked by
        enemy ray
        short_castle is set to true when: right path is clear for castling, right rook has not moved, path not blocked by
        enemy ray
        has_moved (bool) is set to true when the king has moved
        :return:
        """
        if "long_castle" not in conditions:
            conditions["long_castle"] = False
        if "short_castle" not in conditions:
            conditions["short_castle"] = False
        if "has_moved" not in conditions:
            conditions["has_moved"] = True

        ret = []
        if conditions["long_castle"] and not conditions["has_moved"]:
            ret.append(Position(0,2))
        if conditions["short_castle"] and not conditions["has_moved"]:
            ret.append(Position(0,-2))

        return ret
