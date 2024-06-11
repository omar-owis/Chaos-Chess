import math

import pygame
from .helpers import *

from .Pieces.rook import Rook
from .Pieces.bishop import Bishop
from .Pieces.knight import Knight
from .Pieces.queen import Queen
from .Pieces.king import King
from .Pieces.pawn import Pawn
from .Pieces.blank import Blank

from .game_engine import GameEngine


# TODO: change GUI from loop-based to event-based


def position_to_pixels(row: int, col: int):
    pass


class BoardGUI:
    _SCREEN_WIDTH = 640
    _SCREEN_HEIGHT = 640
    _PIECE_SIZE = (_SCREEN_HEIGHT / 8, _SCREEN_WIDTH / 8)

    def __init__(self):
        self.screen = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = GameEngine(self._activate_promotions)
        self.player_color = WHITE
        self.selected_square = ()
        self._promotion_rects = []
        self.promotion_options_active = False

    def start(self):
        pygame.init()

    def _draw_squares(self):
        x_pixel_increment = self._SCREEN_WIDTH / 8
        y_pixel_increment = self._SCREEN_HEIGHT / 8

        for col in range(8):
            for row in range(8):
                if (row + col) % 2 == 0:
                    color = WHITE
                else:
                    color = BROWN
                pygame.draw.rect(self.screen, color, pygame.Rect(x_pixel_increment * row, y_pixel_increment * col,
                                                                 x_pixel_increment, y_pixel_increment))

    def _draw_pieces(self):
        pieces = self.game.board.get_piece_locations()

        for current in pieces:
            self.screen.blit(pygame.transform.scale(current.piece.image, self._PIECE_SIZE),
                             (current.pos.col * (self._SCREEN_WIDTH / 8), current.pos.row * (self._SCREEN_HEIGHT / 8)))

    def _draw_selected_square(self):
        if self.selected_square == ():
            return
        result = self.game.possible_moves(self.selected_square[0], self.selected_square[1])
        for cord in result:
            pygame.draw.circle(self.screen, PURPLE, (cord.col * (self._SCREEN_WIDTH / 8) + 40,
                                                     cord.row * (self._SCREEN_HEIGHT / 8) + 40), 5)

    def _draw_promotion_options(self, row, col, color):
        promotion_pieces = [Queen(color), Knight(color), Rook(color), Bishop(color)]
        self._promotion_rects = []
        direction = 1 if color is WHITE else -1
        for i in range(4):
            rect = pygame.Rect(self._SCREEN_WIDTH / 8 * row, self._SCREEN_HEIGHT / 8 * (col + (-i * direction))
                               , self._SCREEN_WIDTH / 8, self._SCREEN_HEIGHT / 8)
            pygame.draw.rect(self.screen, CREAM, rect)
            self._promotion_rects.append(rect)
            self.screen.blit(pygame.transform.scale(promotion_pieces[i].image, self._PIECE_SIZE),
                             (self._SCREEN_HEIGHT / 8 * row, self._SCREEN_WIDTH / 8 * (col + (-i * direction))))

        if color is WHITE:
            rect = pygame.Rect(self._SCREEN_WIDTH / 8 * row, self._SCREEN_HEIGHT / 8 * (col - 3.5),
                               self._SCREEN_WIDTH / 8, self._SCREEN_HEIGHT / 16)
        else:
            rect = pygame.Rect(self._SCREEN_WIDTH / 8 * row, self._SCREEN_HEIGHT / 8 * (col + 4),
                               self._SCREEN_WIDTH / 8, self._SCREEN_HEIGHT / 16)
        pygame.draw.rect(self.screen, (255, 0, 0), rect)
        self._promotion_rects.append(rect)

        # TODO: draw an 'x' in the center of red rect

    def _handle_promotion_click(self, pos):
        for i, rect in enumerate(self._promotion_rects):
            if rect.collidepoint(pos):
                print(f"Promotion piece {i} clicked!")
                # if cancel then reverse turn
                if not self.game.promote_pawn(self.game.get_last_move().end_pos.row,
                                              self.game.get_last_move().end_pos.col,
                                              i):
                    self.player_color = BLACK if self.player_color is WHITE else WHITE
                self.promotion_options_active = False
                self._promotion_rects = []
                return True
        return False

    def _activate_promotions(self):
        self.promotion_options_active = True

    def run(self):
        self.start()
        y = 0
        x = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    x = math.ceil(mouse_pos[0] / (self._SCREEN_WIDTH / 8)) - 1
                    y = math.ceil(mouse_pos[1] / (self._SCREEN_HEIGHT / 8)) - 1

                    if self.promotion_options_active:
                        self._handle_promotion_click(mouse_pos)
                    elif not self.selected_square and self.game.board.get_piece(y, x):
                        self.selected_square = (y, x)
                    elif self.selected_square:
                        if self.game.play(self.selected_square[0], self.selected_square[1], y, x, self.player_color):
                            self.player_color = BLACK if self.player_color is WHITE else WHITE
                        self.selected_square = ()
                    print("col: " + str(math.ceil(mouse_pos[0] / (self._SCREEN_WIDTH / 8))) +
                          " row: " + str(math.ceil(mouse_pos[1] / (self._SCREEN_HEIGHT / 8))))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.game.undo():
                            self.player_color = BLACK if self.player_color is WHITE else WHITE
                    if event.key == pygame.K_RIGHT:
                        if self.game.redo():
                            self.player_color = BLACK if self.player_color is WHITE else WHITE

                # fill the screen with a color to wipe away anything from last frame
                self.screen.fill(PURPLE)

                # RENDER YOUR GAME HERE
                self._draw_squares()
                self._draw_pieces()
                self._draw_selected_square()
                if self.promotion_options_active:
                    previous_color = BLACK if self.player_color is WHITE else WHITE
                    self._draw_promotion_options(x, y, previous_color)

                # flip() the display to put your work on screen
                pygame.display.flip()

                self.clock.tick(60)  # limits FPS to 60
        pygame.quit()


