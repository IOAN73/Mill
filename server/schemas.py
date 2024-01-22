from enum import StrEnum
from typing import TypeAlias

from pydantic import BaseModel


class Color(StrEnum):
    black = 'black'
    white = 'white'


Position: TypeAlias = tuple[int, int]


class Trick(BaseModel):
    color: Color
    position: Position


class Game(BaseModel):
    tricks_positions: list[Trick]
    tricks_count: int | None = None


class Movement(BaseModel):
    from_position: Position
    to_position: Position


class Kill(BaseModel):
    position: Position
