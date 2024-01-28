from collections import Counter
from enum import StrEnum
from typing import TypeAlias

from pydantic import BaseModel, computed_field

from server.exceptions import (
    CantRemove,
    TrickNotFound,
    TrickSetError,
    TurnError,
)


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
        self._check_should_remove()
        self._check_position_is_free(trick.position)
        if not is_move:
            if self.free_tricks[trick.color] < 1:
                raise TrickNotFound
            self.free_tricks[trick.color] -= 1

        self.tricks.append(trick)
        if not self._check_mills(trick):
            self.turn = ~trick.color
            return
        self.need_remove = True

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
        self._check_should_remove()
        trick = self.tricks.pop(trick_index)
        trick.position = to_position
        self.set_trick(trick, is_move=True)

    def remove_trick(self, position: Position):
        trick_index = self._find_trick(position)
        if self.tricks[trick_index].color == self.turn:
            raise TurnError
        if not self.need_remove:
            raise CantRemove
        self.turn = ~self.tricks[trick_index].color
        self.tricks.pop(trick_index)
        self.need_remove = False

    def _find_trick(self, position: Position) -> int:
        for index, trick in enumerate(self.tricks):
            if trick.position == position:
                return index
        raise TrickNotFound

    def _check_position_is_free(self, position: Position):
        for placed_trick in self.tricks:
            if placed_trick.position == position:
                raise TrickSetError

    def _check_should_remove(self):
        if self.need_remove:
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

    def _check_mills(self, trick: Trick):
        potential_mills = find_potential_mills(trick.position)
        for potential_mill in potential_mills:
            try:
                points = [self._find_trick(point) for point in potential_mill]
                colors = set(self.tricks[point].color for point in points)
                if len(colors - {trick.color}) == 0:
                    return True
            except TrickNotFound:
                continue
        return False

    def _check_trick_can_move(self, position: Position):
        neighbors = desk[position]
        try:
            [self._find_trick(point) for point in neighbors]
            return False
        except TrickNotFound:
            return True

    def _check_color_can_move(self, color: Color):
        tricks_can_move = set(
            self._check_trick_can_move(trick.position)
            for trick in self._user_tricks(color)
        )
        if len(tricks_can_move - {False}) == 0:
            return False
        return True

    def _user_tricks(self, color: Color):
        return [trick for trick in self.tricks if trick.color == color]

    @computed_field
    @property
    def winner(self) -> Color | None:
        black = self._check_color_can_move(Color.black)
        white = self._check_color_can_move(Color.white)
        if not black:
            return Color.white
        if not white:
            return Color.black
        if (
                len(self._user_tricks(Color.white)) < 3
                and self.free_tricks[Color.white] == 0
        ):
            return Color.black
        if (
                len(self._user_tricks(Color.black)) < 3
                and self.free_tricks[Color.black] == 0
        ):
            return Color.white
        return None


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


def find_potential_mills(position: Position):
    positions = {position, *desk[position]}
    for near_position in desk[position]:
        positions.update(desk[near_position])
    xs = [position[0] for position in positions]
    ys = [position[1] for position in positions]
    xs3 = [value for value, count in Counter(xs).items() if count == 3]
    ys3 = [value for value, count in Counter(ys).items() if count == 3]
    mills = []
    for x in xs3:
        mill = tuple(point for point in positions if point[0] == x)
        mills.append(mill)
    for y in ys3:
        mill = tuple(point for point in positions if point[1] == y)
        mills.append(mill)
    return [mill for mill in mills if position in mill]


if __name__ == '__main__':
    print(find_potential_mills((1, 1)))
