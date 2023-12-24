from .board import *
from .helpers import *
from .data_classes import *

# TODO: Pawn Promotions
# TODO: Add timers
# TODO: Squares deletions: chance that board losses (1-3) clustered squares
# TODO: Dynamic board, every set number of turns the board will increase in rows or columns
# TODO: Code Optimizations
# TODO: a whole lotta refactoring

# Square Deletions: can occur at any moment (not turn-based), chance of deletion is dependent on the sum of time for
# both players (lower the sum, the higher the chance of occurrence threshold based), if hole spawned under piece push back
# towards piece's base, window should have a literal hole in it to display what ever is behind the game window
# threshold based system: when sum drops below 5 minutes chance is 10% + some formula based on time. When sum drops below
# 3 minutes chance is 30% + same formula, so on. Tweak thresholds and formula for best gameplay
# Row and Column additions: new row/column is added to the board from the outer edges, new row/column is pushed in to
# the middle, adding new row or column increases window size accordingly
class GameEngine:
    # TODO(bugfix): white king dont see pawn checks
    # TODO(bugfix): black playing an illegal move while in check crashes client
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        self.history: list[Move] = []
        self.pinned_pieces: list[PinnedPiece] = []
        self.check_source: list[Position] = []
        self.en_passant_square: Position = None

    def possible_moves(self, row: int, col: int) -> list[Position]:
        piece = self.board.get_piece(row, col)
        self._evaluate_checks_and_pins(piece.color)

        block_squares = []
        if piece is None:
            return []
        if len(self.check_source) > 1 and not isinstance(piece, King):
            return []
        if len(self.check_source) == 1:
            king = self.board.white_king if piece.color is WHITE else self.board.black_king
            block_squares = self.board.inbetween_squares(king, self.check_source[0])

        moves = []
        directions = piece.capture_directions
        pinned_direction = self._extract_pinned_direction(piece)

        if isinstance(piece, Pawn):
            left_capture, right_capture = self._evaluate_pawn_captures(piece, row, col)
            up = 1 if piece.color is WHITE else -1
            up_square = self.board.get_piece(row+up, col) is None
            two_up_square = self.board.get_piece(row+2*up, col) is None
            has_moved = self._has_moved(piece)


            # add additional directions
            relative_moves = piece.conditional_directions(has_moved=has_moved,
                                                          left_capture=left_capture,
                                                          right_capture=right_capture,
                                                          up_square=up_square,
                                                          two_up_square= two_up_square,
                                                          pin_direction=pinned_direction)
            for rm in relative_moves:
                rm = rm if piece.color is WHITE else -rm
                if not block_squares or Position(row, col) + rm in block_squares: moves.append(Position(row, col) + rm)

        elif isinstance(piece, King):
            x = 1 if piece.color is WHITE else -1
            relative_moves = piece.conditional_directions(has_moved=self._has_moved(piece),
                                                          long_castle=self._long_castling_rights(piece.color),
                                                          short_castle=self._short_castling_rights(piece.color))
            for rm in relative_moves:
                moves.append(Position(row, col) + rm)

        for direction in directions:
            if (pinned_direction is not None
                and direction not in [pinned_direction, -pinned_direction]):
                continue
            # convert direction from piece relative to position
            direction = direction if piece.color is WHITE else -direction
            position = Position(row, col) + direction
            # if square is out of bounds continue
            if not self.board.inbound(position):
                continue

            other = self.board.get_piece(position.row, position.col)

            if isinstance(piece, King):
                if not self._is_square_attacked(position, piece.color, ignore_king=True) and (other is None
                or other.color is not piece.color):
                    moves.append(position)
            else:
                if other is not None:
                    if other.color is not piece.color and not isinstance(piece, Pawn):
                        if not block_squares or position in block_squares: moves.append(position)
                    continue
                if not block_squares or position in block_squares: moves.append(position)

            if piece.extend_direction:
                # while direction + direction not occupied, add to moves
                extend_direction: Position = position + direction

                while (self.board.inbound(extend_direction)
                       and (other := self.board.get_piece(extend_direction.row, extend_direction.col)) is None):
                    if not block_squares or extend_direction in block_squares: moves.append(extend_direction)
                    extend_direction += direction

                # add capture move
                if other is not None and other.color is not piece.color and not isinstance(piece, Pawn):
                    if not block_squares or extend_direction in block_squares: moves.append(extend_direction)

        return moves

    def play(self, start_row, start_col ,end_row, end_col, turn):
        piece = self.board.get_piece(start_row, start_col)
        self.en_passant_square = None
        if turn is not self.turn:
            print("Not player's turn")
            return False
        if start_row == end_row and start_col == end_col:
            return False
        if piece is None:
            print(f"No piece on {start_row}, {start_col}")
            return False
        if piece.color is not turn:
            print("Not player's piece")
            return False
        # check if that piece can move there
        allowable_moves = self.possible_moves(start_row, start_col)
        if Position(end_row, end_col) not in allowable_moves:
            print(f"Illegal move")
            return False

        if isinstance(piece, Pawn):
            direction = UP if piece.color is WHITE else DOWN
            capture_direction = Position(start_row - end_row, start_col - end_col)
            # detect en passant squares
            if abs(start_row-end_row) == 2:
                self.en_passant_square = Position(start_row, start_col) + direction
            # capture en passant move
            elif (abs(capture_direction.row) == abs(capture_direction.col) and
                  self.board.get_piece(end_row, end_col) is None):
                pos = Position(end_row, end_col) - direction
                self.board.set_square(pos.row, pos.col, None)

        # move piece to that square
        self.history.append(Move(piece, Position(start_row,start_col), Position(end_row, end_col)))
        self.board.set_square(start_row, start_col, None)
        self.board.set_square(end_row, end_col, piece)
        self._try_promote_pawn(end_row, end_col, piece, Queen(piece.color))

        other = BLACK if turn is WHITE else WHITE

        # change turn
        self.turn = other
        return True


    def _has_moved(self, piece):
        for move in self.history:
            if move.piece == piece:
                return True
        return False

    def _long_castling_rights(self, color) -> bool:
        """
        given color, the function will calculate if that given color can long castle.
        This function does not factor in if the king has moved.
        :param color: rgb
        :return: Boolean
        """
        r = 0 if color is WHITE else 7
        square1 = self.board.get_piece(r,5)
        square2 = self.board.get_piece(r,6)
        rook = self.board.get_piece(r, 7)

        if rook is None or self._has_moved(rook):
            return False

        if square1 is not None or square2 is not None:
            return False

        if self._is_square_attacked(Position(r,5), color) or self._is_square_attacked(Position(r,6), color):
            return False

        return True

    def _short_castling_rights(self, color) -> bool:
        """
        given color, the function will calculate if that given color can short castle. This function does not factor in if the
        king has moved.
        :param color: rgb
        :return: Boolean
        """
        r = 0 if color is WHITE else 7
        square1 = self.board.get_piece(r, 1)
        square2 = self.board.get_piece(r, 2)
        rook = self.board.get_piece(r, 0)

        if rook is None or self._has_moved(rook):
            return False

        if square1 is not None or square2 is not None:
            return False

        if self._is_square_attacked(Position(r, 1), color) or self._is_square_attacked(Position(r, 2), color):
            return False

        return True

    def _is_square_attacked(self, pos: Position, color, ignore_king=False) -> bool:
        """
        Given position on the board and an ally color. The function will calculate if that square is under attack by
        enemy colors
        :param pos: Position
        :param color: rgb
        :return: Boolean
        """
        for direction in ALL_DIRECTIONS:
            # convert direction from piece relative to position
            extend_direction = pos + direction
            square = None

            while (self.board.inbound(extend_direction)
                   and ((square := self.board.get_piece(extend_direction.row, extend_direction.col)) is None
                   or (ignore_king and isinstance(square, King) and square.color is color))):
                extend_direction += direction

            if square is not None and square.color is not color and direction in square.capture_directions:
                return True

        for k_direction in KNIGHT_DIRECTIONS:
            position = pos + k_direction
            if not self.board.inbound(position):
                continue
            square = self.board.get_piece(position.row, position.col)
            if square is None:
                continue
            if isinstance(square, Knight) and square.color is not color:
                return True

        # check for pawn attacks
        up = 1
        # left square of king
        right = Position(up, up)
        right_pos = pos + right if color is WHITE else pos - right
        if self.board.inbound(right_pos):
            square = self.board.get_piece(right_pos.row, right_pos.col)
            if (square is not None
                    and isinstance(square, Pawn)
                    and square.color is not color):
                return True
        # right square of pawn
        left = Position(up, -up)
        left_pos = pos + left if color is WHITE else pos - left
        if self.board.inbound(left_pos):
            square = self.board.get_piece(left_pos.row, left_pos.col)
            if (square is not None
                    and isinstance(square, Pawn)
                    and square.color is not color):
                return True
        return False

    def _evaluate_checks_and_pins(self, color):
        pos = self.board.white_king if color is WHITE else self.board.black_king
        self.check_source.clear()
        self.pinned_pieces.clear()
        for direction in ALL_DIRECTIONS:
            # convert direction from piece relative to position
            possible_pins: list[Piece] = []

            # while direction + direction not occupied, add to moves
            extend_direction: Position = pos + direction

            while self.board.inbound(extend_direction):
                square = self.board.get_piece(extend_direction.row, extend_direction.col)
                if square is not None:
                    if color is not square.color and direction in square.capture_directions:
                        if not extend_direction.is_direction() and not square.extend_direction:
                            break
                        if not possible_pins:
                            self.check_source.append(extend_direction)
                        elif len(possible_pins) == 1:
                            self.pinned_pieces.append(PinnedPiece(possible_pins[0],direction))
                        break
                    elif color is square.color:
                        possible_pins.append(square)
                    else:
                        break
                extend_direction += direction
            possible_pins.clear()

        # check for knight checks
        for k_direction in KNIGHT_DIRECTIONS:
            position = pos + k_direction
            if not self.board.inbound(position):
                continue
            square = self.board.get_piece(position.row, position.col)
            if square is None:
                continue
            if isinstance(square, Knight) and square.color is not color:
                self.check_source.append(position)

        # check for pawn checks
        up = 1
        # left square of king
        right = Position(up, up)
        right_pos = pos + right if color is WHITE else pos - right
        if self.board.inbound(right_pos):
            square = self.board.get_piece(right_pos.row, right_pos.col)
            if (square is not None
            and isinstance(square, Pawn)
            and square.color is not color):
                self.check_source.append(right)
        # right square of pawn
        left = Position(up, -up)
        left_pos = pos + left if color is WHITE else pos - left
        if self.board.inbound(left_pos):
            square = self.board.get_piece(left_pos.row, left_pos.col)
            if (square is not None
            and isinstance(square, Pawn)
            and square.color is not color):
                self.check_source.append(left)

    def _extract_pinned_direction(self, piece: Piece):
        if self.pinned_pieces:
            for pinned in self.pinned_pieces:
                if piece == pinned.piece:
                    return pinned.direction
        return None

    def _evaluate_pawn_captures(self, piece, row, col):
        # left square of pawn
        left_dir = UP_LEFT if piece.color is WHITE else DOWN_LEFT
        left = Position(row, col) + left_dir
        left_capture = (left.col >= 0 and
                        ((self.board.get_piece(left.row, left.col) is not None and
                          self.board.get_piece(left.row, left.col).color != piece.color)
                         or left == self.en_passant_square))

        # right square of pawn
        right_dir = UP_RIGHT if piece.color is WHITE else DOWN_RIGHT
        right = Position(row, col) + right_dir
        right_capture = (right.col < self.board.col_size() and
                         ((self.board.get_piece(right.row, right.col) is not None and
                           self.board.get_piece(right.row, right.col).color != piece.color)
                          or right == self.en_passant_square))
        return left_capture, right_capture

    def _try_promote_pawn(self, row, col, piece, promotion_piece):
        if not isinstance(piece, Pawn):
            return

        promote_row = self.board.col_size()-1 if piece.color is WHITE else 0
        if row == promote_row:
            self.board.set_square(row, col, promotion_piece)