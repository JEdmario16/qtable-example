import pygame
from typing import Self

from qtable_example.enums import Unit

# Margin order is: top, right, bottom, left (clockwise)


class UIElement:

    def __init__(
        self,
        *,
        parent: Self | None = None,
        surface: pygame.Surface | None = None,
        width: int = 0,
        height: int = 0,
        position: tuple[int, int] = (0, 0),
        margin: tuple[int, int] | tuple[int, int, int, int] | int = 0,
        margin_unity: Unit | int = Unit.PIXEL,
        size_unity: Unit | int = Unit.PIXEL,
        padding: tuple[int, int] | tuple[int, int, int, int] | int = 0,
        padding_unity: Unit | int = Unit.PIXEL,
        background_color: tuple[int, int, int] = (255, 255, 255),
    ):

        if not surface and not parent:
            raise ValueError("Either surface or parent must be provided.")

        self.base_surface: pygame.Surface = parent.base_surface if parent else surface
        self.parent: Self | None = parent

        self.width, self.height = self._size_calc(
            unit=size_unity,
            width=width,
            height=height,
        )

        self.margin = self.__handle_margin(
            margin=margin,
            margin_unity=margin_unity,
        )

        self.position = self._calculate_position(
            position=position,
            margin=self.margin,
            margin_unity=margin_unity,
            parent=parent,
        )

        self.image: pygame.Surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )

        self.background_color = background_color

    def __handle_unit(self, unit: Unit | int):
        if isinstance(unit, int):
            try:
                return Unit(unit)
            except ValueError:
                raise ValueError(
                    f"Invalid unit value: {unit}. Must be an int or Unit enum."
                )
        elif isinstance(unit, Unit):
            return unit
        raise ValueError(
            f"Invalid unit type: {type(unit)}. Must be an int or Unit enum."
        )

    def __handle_margin(
        self,
        margin: tuple[int, int] | tuple[int, int, int, int] | int,
        margin_unity: Unit | int,
    ) -> tuple[int, int, int, int]:
        """Handle the margin based on the unit and margin properties."""
        unit = self.__handle_unit(margin_unity)
        handled_margin = (0, 0, 0, 0)

        if isinstance(margin, int):
            handled_margin = (margin, margin, margin, margin)
        elif len(margin) == 2:
            handled_margin = (margin[0], margin[1], margin[0], margin[1])
        elif len(margin) == 4:
            handled_margin = (margin[0], margin[1], margin[2], margin[3])
        else:
            raise ValueError("Margin must be an int or a tuple of 2 or 4 ints.")

        match unit:
            case Unit.PIXEL:
                return handled_margin
            case Unit.PERCENT:
                screen_width, screen_height = self.parent.width, (
                    self.parent.height if self.parent else self.base_surface.get_size()
                )
                m = (
                    int(screen_width * (handled_margin[0] / 100)),
                    int(screen_height * (handled_margin[1] / 100)),
                    int(screen_width * (handled_margin[2] / 100)),
                    int(screen_height * (handled_margin[3] / 100)),
                )
                print(f"Margin in pixels: {m}")
                return m
            case _:
                raise ValueError("Invalid margin mode. Use 'pixel' or 'percent'.")

    def _size_calc(
        self,
        unit: Unit | int,
        width: int,
        height: int,
    ) -> tuple[int, int]:
        """
        Calculate the size of the element based on the unit and size properties.
        """
        unit = self.__handle_unit(unit)
        match unit:
            case Unit.PIXEL:
                return width, height
            case Unit.PERCENT:
                screen_width, screen_height = self.base_surface.get_size()
                return int(screen_width * (width / 100)), int(
                    screen_height * (height / 100)
                )
            case _:
                raise ValueError("Invalid size mode. Use 'pixel' or 'percent'.")

    def _calculate_position(
        self,
        position: tuple[int, int],
        margin: tuple[int, int] | tuple[int, int, int, int] | int,
        margin_unity: Unit | int,
        parent: Self | None = None,
    ) -> tuple[int, int]:
        """
        Calculate the position of the element based on the parent and margin.
        """
        return (
            position[0] + margin[0],
            position[1] + margin[1],
        )

    def update(self):
        raise NotImplementedError(
            "The update method must be implemented in the subclass."
        )

    def draw(self):
        """
        Draw the element on the base surface.
        """
        if self.background_color:
            self.image.fill(self.background_color)
        self.base_surface.blit(self.image, self.rect)

    @property
    def rect(self) -> pygame.Rect:
        """
        Get the rect of the element.
        """
        return self.image.get_rect(topleft=self.position)

    @property
    def size(self) -> tuple[int, int]:
        """
        Get the size of the element.
        """
        return self.width, self.height

    @property
    def surface(self) -> pygame.Surface:
        """
        Get the surface of the element.
        """
        return self.image
