from .Pieces.rook import Rook
from .Pieces.bishop import Bishop
from .Pieces.knight import Knight
from .Pieces.queen import Queen
from .Pieces.king import King
from .Pieces.pawn import Pawn
from .Pieces.blank import Blank

from .helpers import *

from .data_classes import *


def convert_piece_to_char(piece: 'Piece') -> str:
    result = ''
    match piece:
        case King():
            result = 'k'
        case Knight():
            result = 'n'
        case Bishop():
            result = 'b'
        case Rook():
            result = 'r'
        case Queen():
            result = 'q'
        case Pawn():
            result = 'p'

    if piece.color is WHITE:
        result = result.upper()

    return result


class Board:
    def __init__(self):
        self.board = [[Rook(WHITE), Knight(WHITE), Bishop(WHITE), King(WHITE),
                       Queen(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
                      [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
                       Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
                       Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
                      [Rook(BLACK), Knight(BLACK), Bishop(BLACK), King(BLACK),
                       Queen(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]]
        self.white_king: Position = Position(0,3)
        self.black_king: Position = Position(7,3)

    def get_piece_locations(self):
        """
        returns a list of all the piece locations for GUI to draw
        :return:
        """
        ret = []
        r = 0
        c = 0
        for row in self.board:
            for element in row:
                if element is not None:
                    ret.append(PieceLocation(element, Position(r, c)))
                c += 1
            r += 1
            c = 0
        return ret

    def get_piece(self, row: int, col: int) -> Piece:
        if not self.inbound(Position(row, col)):
            return None
        return self.board[row][col]

    def set_square(self, row: int, col: int, piece) -> None:
        if isinstance(piece, King):
            if piece.color is WHITE:
                self.white_king = Position(row, col)
            elif piece.color is BLACK:
                self.black_king = Position(row, col)
        self.board[row][col] = piece

    def inbound(self, pos: Position) -> bool:
        return 0 <= pos.row < len(self.board) and 0 <= pos.col < len(self.board[0])

    def inbetween_squares(self, start: Position, end: Position) -> list[Position]:
        """
        Given a start square and an end square, the function will return a list of squares inbetween the two given
        squares
        :param start: Position
        :param end: Position
        :return: List[Position]
        """
        inbetween_squares_list = []

        # Ensure start and end positions are different
        if start.row == end.row and start.col == end.col:
            return inbetween_squares_list
        if not self.inbound(start) or not self.inbound(end):
            return inbetween_squares_list

        # Determine the direction of movement (horizontal, vertical, or diagonal)
        direction = (end - start).convert_to_direction()

        extended_direction = start + direction
        while extended_direction.row != end.row or extended_direction.col != end.col:
            inbetween_squares_list.append(extended_direction)
            extended_direction += direction
        inbetween_squares_list.append(end)

        return inbetween_squares_list

    def row_size(self):
        return len(self.board)

    def col_size(self):
        return len(self.board[0])

    def delete_square(self, row, col):
        self.board[row][col] = Blank(None)

    def to_static_fen(self) -> str:
        counter = 0
        result = ''
        for row in self.board:
            for tile in row:
                if not tile:
                    counter += 1
                else:
                    if counter > 0:
                        result += str(counter)
                        counter = 0
                    result += convert_piece_to_char(tile)
            if counter > 0:
                result += str(counter)
                counter = 0
            result += '/'

        return (result[:-1])[::-1]
