from enum import StrEnum
from typing import TypeAlias

from pydantic import BaseModel

from server.exceptions import TurnError, TrickSetError, TrickNotFound


class Color(StrEnum):
    black = 'black'
    white = 'white'

    def __invert__(self):
        match self.value:
            case self.black:
                return self.white
            case self.white:
                return self.black

Position: TypeAlias = tuple[int, int]


class Trick(BaseModel):
    color: Color
    position: Position


class Game(BaseModel):
    turn: Color = Color.white
    tricks: list[Trick] = []
    white_free_tricks_count: int = 9
    black_free_tricks_count: int = 9

    def set_trick(self, trick: Trick, is_move: bool = False):
        if self.turn != trick.color:
            raise TurnError
        self._check_position_is_free(trick.position)
        match trick.color:
            case Color.white:
                if not is_move:
                    if self.white_free_tricks_count < 1:
                        raise TrickNotFound
                    self.white_free_tricks_count -= 1
            case Color.black:
                if not is_move:
                    if self.black_free_tricks_count < 1:
                        raise TrickNotFound
                    self.black_free_tricks_count -= 1
        self.turn = ~trick.color
        self.tricks.append(trick)

    def move_trick(
            self,
            from_position: Position,
            to_position: Position,
    ):
        self._check_position_is_free(to_position)
        trick_index = self._find_trick(from_position)
        trick = self.tricks.pop(trick_index)
        if trick.color != self.turn:
            self.set_trick(trick)
            raise TurnError
        trick.position = to_position
        self.set_trick(trick)

    def _find_trick(self, position: Position) -> int:
        for index, trick in enumerate(self.tricks):
            if trick.position == position:
                return index
        raise TrickNotFound

    def _check_position_is_free(self, position: Position):
        for placed_trick in self.tricks:
            if placed_trick.position == position:
                raise TrickSetError


class Movement(BaseModel):
    from_position: Position
    to_position: Position


desk: dict[Position, list[Position]] = {
    (0, 0): [(3, 0), (0, 3)],
    (3, 0): [(0, 0), (3, 1), (6, 0)],
    (6, 0): [(3, 0), (6, 3)],
    (1, 1): [(1, 3), (3, 1)],
    (3, 1): [(1, 1), (3, 0), (3, 2), (5, 1)],
    (5, 1): [(3, 1), (5, 3)],
    (2, 2): [(2, 3), (3, 2)],
    (3, 2): [(2, 2), (3, 1), (4, 2)],
    (4, 2): [(3, 2), (4, 3)],
    (0, 3): [(0, 6), (0, 0), (1, 3)],
    (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
    (2, 3): [(1, 3), (2, 4), (2, 2)],
    (4, 3): [(5, 3), (4, 4), (4, 2)],
    (5, 3): [(4, 3), (5, 5), (5, 1), (6, 3)],
    (6, 3): [(5, 3), (6, 6), (6, 0)],
    (2, 4): [(2, 3), (3, 4)],
    (3, 4): [(2, 4), (3, 5), (4, 4)],
    (4, 4): [(3, 4), (4, 3)],
    (1, 5): [(1, 3), (3, 5)],
    (3, 5): [(1, 5), (3, 6), (3, 4), (5, 5)],
    (5, 5): [(3, 5), (5, 3)],
    (0, 6): [(0, 3), (3, 6)],
    (3, 6): [(0, 6), (3, 5), (6, 6)],
    (6, 6): [(3, 6), (6, 3)]
}
