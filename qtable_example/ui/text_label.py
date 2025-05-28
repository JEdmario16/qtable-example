import pygame

from qtable_example.ui.ui_element import UIElement
from qtable_example.enums import Unit, TextAlign

from typing import Literal


class TextLabel(UIElement):
    """
    A simple text label UI element.
    """

    def __init__(
        self,
        *,
        text: str = "",
        font_size: int = 24,
        font_color: tuple[int, int, int] = (0, 0, 0),
        position: tuple[int, int] = (0, 0),
        text_align_x: TextAlign = TextAlign.LEFT,
        text_align_y: TextAlign = TextAlign.TOP,
        background_color: tuple[int, int, int] | None = None,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.background_color = background_color

        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.Font(None, self.font_size)
        self._text_surface = self.font.render(self.text, True, self.font_color)
        self.text_align_x = text_align_x
        self.text_align_y = text_align_y
        self.needs_redraw = True

        if text_align_x or text_align_y:  # then ignores position parameter
            position = self.set_position(text_align_x, text_align_y, position)
            self.position = position

    def set_position(
        self,
        text_align_x: TextAlign | None = None,
        text_align_y: TextAlign | None = None,
        position: tuple[int, int] = (0, 0),
    ):
        rect_topleft = list(position)

        # handle text alignment
        parent_w = self.parent.width if self.parent else self.base_surface.get_width()
        parent_h = self.parent.height if self.parent else self.base_surface.get_height()
        print(f"Parent size: {parent_w}x{parent_h}")

        match text_align_x:
            case TextAlign.LEFT:
                rect_topleft = (0, 0)
            case TextAlign.CENTER:
                rect_topleft = (parent_w // 2, rect_topleft[1])

                # ajusta o topleft para o centro do texto
                rect_topleft = (
                    rect_topleft[0] - self._text_surface.get_width() // 2,
                    rect_topleft[1],
                )

            case TextAlign.RIGHT:
                rect_topleft = (parent_w, 0)

        match text_align_y:
            case TextAlign.TOP:
                rect_topleft = (0, 0)
            case TextAlign.CENTER:
                rect_topleft = (
                    rect_topleft[0],
                    parent_h // 2,
                )
                # ajusta o topleft para o centro do texto
                rect_topleft = (
                    rect_topleft[0],
                    rect_topleft[1] - self._text_surface.get_height() // 2,
                )

            case TextAlign.BOTTOM:
                rect_topleft = (0, parent_h)

        # adds the margin to the position
        if self.margin:
            rect_topleft = (
                rect_topleft[0] + self.margin[0],
                rect_topleft[1] + self.margin[1],
            )
        print(f"TextLabel position set to: {rect_topleft}")
        return rect_topleft

    def set_text(self, text: str):
        self.text = text
        self.needs_redraw = True

    def set_color(self, color: tuple[int, int, int]):
        """Set the font color."""
        self.font_color = color
        self.needs_redraw = True

    def update(self):
        """Update the text label if needed."""
        if self.needs_redraw:
            self.image = self.font.render(
                self.text, True, self.font_color, self.background_color
            )
            self.needs_redraw = False

            self.base_surface.blit(self.image, self.rect)
