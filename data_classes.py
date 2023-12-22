from dataclasses import dataclass
from .Pieces.piece import Piece


@dataclass
class Position:
    row: int
    col: int

    def flip(self):
        return Position(self.col, self.row)

    def is_direction(self):
        return (abs(self.row) == 1 or self.row == 0) and (abs(self.col) == 1 and self.col == 0)

    def convert_to_direction(self):
        # if given knight direction return self
        if (abs(self.row) == 2 and abs(self.col) == 1
            or abs(self.row) == 1 and abs(self.col) == 2):
            return self

        r = 1 if self.row > 0 else -1 if self.row < 0 else 0
        c = 1 if self.col > 0 else -1 if self.col < 0 else 0
        return Position(r, c)



    def __add__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        return Position(self.row - other.row, self.col - other.col)

    def __neg__(self):
        return Position(-self.row, -self.col)

@dataclass
class PieceLocation:
    piece: Piece
    pos: Position


@dataclass
class Move:
    piece: Piece
    start_pos: Position
    end_pos: Position

@dataclass
class PinnedPiece:
    piece: Piece
    direction: Position
