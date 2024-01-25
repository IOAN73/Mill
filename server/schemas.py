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
    free_tricks: dict[Color, int] = {
        Color.white: 9,
        Color.black: 9,
    }
    need_remove: bool = False

    def set_trick(self, trick: Trick, is_move: bool = False):
        self._check_turn(trick.color)
        self._check_position_is_free(trick.position)
        if not is_move:
            if self.free_tricks[trick.color] < 1:
                raise TrickNotFound
            self.free_tricks[trick.color] -= 1

        self.turn = ~trick.color
        self.tricks.append(trick)

    def move_trick(
            self,
            from_position: Position,
            to_position: Position,
    ):
        self._check_no_free_tricks()
        self._check_position_is_accessible(from_position, to_position)
        self._check_position_is_free(to_position)
        trick_index = self._find_trick(from_position)
        self._check_turn(self.tricks[trick_index].color)
        trick = self.tricks.pop(trick_index)
        trick.position = to_position
        self.set_trick(trick, is_move=True)
        self.turn = ~trick.color

    def _find_trick(self, position: Position) -> int:
        for index, trick in enumerate(self.tricks):
            if trick.position == position:
                return index
        raise TrickNotFound

    def _check_position_is_free(self, position: Position):
        for placed_trick in self.tricks:
            if placed_trick.position == position:
                raise TrickSetError

    @staticmethod
    def _check_position_is_accessible(
            from_position: Position,
            to_position: Position,
    ):
        if to_position not in desk[from_position]:
            raise TrickSetError

    def _check_turn(self, color: Color):
        if self.turn != color:
            raise TurnError

    def _check_no_free_tricks(self):
        for tricks_count in self.free_tricks.values():
            if tricks_count > 0:
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
