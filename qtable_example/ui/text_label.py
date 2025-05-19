import pygame

from typing import Literal


class TextLabel(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        position: tuple[int, int] | None = None,
        align_text: Literal["left", "center", "right"] | None = "left",
        parent_surface: pygame.Surface | None = None,
        padding: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        super().__init__()

        self.parent_surface = parent_surface
        self.text = text
        self.font = font
        self.color = color
        self.image = self.font.render(self.text, True, self.color)
        self.padding = padding

        if not position and not align_text:
            raise ValueError(
                "You must provide a position or align_text to the TextLabel."
            )

        if not position:
            position = self.set_position(align_text)

        self.position = position
        self.align_text = align_text
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.position)

    def set_position(
        self,
        align_text: Literal["left", "center", "right"] | None = None,
    ) -> tuple[int, int]:

        rect_topleft = tuple()
        if align_text == "left":
            rect_topleft = (0, 0)
        elif align_text == "center":
            rect_topleft = (
                self.parent_surface.get_width() // 2,
                0,
            )

            # aplica um offset para do centro para o topo
            rect_topleft = (
                rect_topleft[0] - self.image.get_width() // 2,
                rect_topleft[1],
            )
            
        elif align_text == "right":
            rect_topleft = self.parent_surface.get_size()
        else:
            raise ValueError("Invalid alignment. Use 'left', 'center', or 'right'.")

        if any(self.padding):
            rect_topleft = (
                rect_topleft[0] + self.padding[0],
                rect_topleft[1] + self.padding[1],
            )


        return rect_topleft
