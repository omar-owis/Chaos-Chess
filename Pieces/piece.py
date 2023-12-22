
from abc import ABC, abstractmethod
import pygame
import os

'''
Notes:
 - chess engine handles direction extension, since the piece object
 has no knowledge surrounding pieces on the board
 - pins are handled by chess engine, since the piece object
 has no knowledge surrounding pieces on the boards
 - promotions are handled by chess engine since it is not considered a direction/move
'''

class Piece(ABC):
    def __init__(self, color):
        self.color = color
        self.image = None
        self.capture_directions: list[Position] = []
        self.extend_direction = False

    def __eq__(self, other):
        if isinstance(other, Piece):
            return id(self) == id(other)
        return False

    @abstractmethod
    def conditional_directions(self, **conditions):
        """
        given a set of conditions the function will return additional directions to the caller
        :return: [(row, col), (row, col), ...]
        """
        pass