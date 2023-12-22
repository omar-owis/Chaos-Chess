from ..helpers import *

from .piece import *


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.capture_directions = []
        self.extend_direction = False
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/white-pawn.png"))\
            if color is WHITE else pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/black-pawn.png"))

    def conditional_directions(self, **conditions):
        """
        conditions handled by pawn: left_capture (bool), right_capture (bool), has_moved (bool), up_square (bool),
        pin_direction (Position)
        left_capture is set to true when a piece could be captured to the left, either by en passant or regularly
        right_capture is set to true when a piece could be captured to the right, either by en passant or regularly
        has_moved is set to true when the pawn has moved
        up_square is set to true when the up direction square is empty
        two_up_square is set to true when the (2,0) square is empty
        pin_direction is set to the direction the pawn is pinned to. If pawn is not pinned it is set to None
        :return: [(row, col), (row, col), ...]
        """
        if "left_capture" not in conditions:
            conditions["left_capture"] = False
        if "right_capture" not in conditions:
            conditions["right_capture"] = False
        if "has_moved" not in conditions:
            conditions["has_moved"] = True
        if "up_square" not in conditions:
            conditions["up_square"] = False
        if "two_up_square" not in conditions:
            conditions["two_up_square"] = False
        if "pin_direction" not in conditions:
            conditions["pin_direction"] = None

        ret = []
        if (conditions["left_capture"] and
            (conditions["pin_direction"] is None or conditions["pin_direction"] in [UP_LEFT, DOWN_LEFT])):
            left = UP_LEFT if self.color is WHITE else UP_RIGHT
            ret.append(left)
        if (conditions["right_capture"] and
            (conditions["pin_direction"] is None or conditions["pin_direction"] in [UP_RIGHT, DOWN_RIGHT])):
            right = UP_RIGHT if self.color is WHITE else UP_LEFT
            ret.append(right)
        if (not conditions["has_moved"] and conditions["up_square"] and conditions["two_up_square"]
            and (conditions["pin_direction"] is None or conditions["pin_direction"] in [UP, DOWN])):
            ret.append(Position(2,0))
        if (conditions["up_square"]
            and (conditions["pin_direction"] is None or conditions["pin_direction"] in [UP, DOWN])):
            ret.append(Position(1, 0))
        return ret
