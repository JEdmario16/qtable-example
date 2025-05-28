from enum import Enum


class Directions(Enum):
    """Enum for directions."""

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7


class Unit(Enum):
    """Enum for size modes."""

    PIXEL = 0
    PERCENT = 1


class TextAlign(Enum):
    """Enum for text alignment."""

    LEFT = 0
    CENTER = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
