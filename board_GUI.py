import math

import pygame
from .helpers import *

from .game_engine import GameEngine

def position_to_pixels(row: int, col: int):
    pass

class BoardGUI:
    _SCREEN_WIDTH = 640
    _SCREEN_HEIGHT = 640
    _PIECE_SIZE = (_SCREEN_HEIGHT/8, _SCREEN_WIDTH/8)
    def __init__(self):
        self.screen = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = GameEngine()
        self.player_color = WHITE
        self.selected_square = ()

    def start(self):
        pygame.init()

    def _draw_squares(self):
        x_pixel_increment = self._SCREEN_WIDTH/8
        y_pixel_increment = self._SCREEN_HEIGHT/8

        for col in range(8):
            for row in range(8):
                if (row+col) % 2 == 0:
                    color = WHITE
                else:
                    color = BROWN
                pygame.draw.rect(self.screen, color, pygame.Rect(x_pixel_increment * row, y_pixel_increment * col,
                                                                   x_pixel_increment, y_pixel_increment))
    def _draw_pieces(self):
        pieces = self.game.board.get_piece_locations()

        for current in pieces:
            self.screen.blit(pygame.transform.scale(current.piece.image, self._PIECE_SIZE),
                             (current.pos.col * (self._SCREEN_WIDTH/8), current.pos.row * (self._SCREEN_HEIGHT/8)))

    def _draw_selected_square(self):
        if self.selected_square == ():
            return
        result = self.game.possible_moves(self.selected_square[0], self.selected_square[1])
        for cord in result:
            pygame.draw.circle(self.screen, PURPLE, (cord.col * (self._SCREEN_WIDTH/8)+40,
                                                     cord.row * (self._SCREEN_HEIGHT/8)+40), 5)



    def run(self):
        self.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    r = math.ceil(pygame.mouse.get_pos()[1] / (self._SCREEN_HEIGHT/8))-1
                    c = math.ceil(pygame.mouse.get_pos()[0] / (self._SCREEN_WIDTH/ 8))-1
                    if not self.selected_square and self.game.board.get_piece(r,c):
                        self.selected_square = (r, c)
                    elif self.selected_square:
                        if self.game.play(self.selected_square[0], self.selected_square[1], r, c, self.player_color):
                            self.player_color = BLACK if self.player_color is WHITE else WHITE
                        self.selected_square = ()
                    print("col: " + str(math.ceil(pygame.mouse.get_pos()[0] / (self._SCREEN_WIDTH/8))) +
                          " row: " + str(math.ceil(pygame.mouse.get_pos()[1] / (self._SCREEN_HEIGHT / 8))))

                # fill the screen with a color to wipe away anything from last frame
                self.screen.fill(PURPLE)

                # RENDER YOUR GAME HERE
                self._draw_squares()
                self._draw_pieces()
                self._draw_selected_square()

                # flip() the display to put your work on screen
                pygame.display.flip()

                self.clock.tick(60)  # limits FPS to 60
        pygame.quit()