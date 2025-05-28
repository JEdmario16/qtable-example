import pygame

from qtable_example.ui.ui_element import UIElement
from qtable_example.enums import Unit


class Container(UIElement):

    def __init__(
        self,
        *,
        parent: UIElement | None = None,
        surface: pygame.Surface | None = None,
        width: int = 0,
        height: int = 0,
        position: tuple[int, int] = (0, 0),
        margin: tuple[int, int] | tuple[int, int, int, int] | int = 0,
        margin_unity: int | str = Unit.PIXEL,
        size_unity: int | str = Unit.PIXEL,
        background_color: tuple[int, int, int] = (255, 255, 255),
    ):
        """
        Initializes a Container UI element.

        Parameters:
            parent (UIElement | None): The parent UI element, if any.
            surface (pygame.Surface | None): The surface to draw on, if not using a parent.
            width (int): Width of the container.
            height (int): Height of the container.
            position (tuple[int, int]): Position of the container on the screen.
            margin (tuple[int, int] | tuple[int, int, int, int] | int): Margin around the container.
            margin_unity (int | str): Unit for margin measurement, default is "pixel".
            size_unity (int | str): Unit for size measurement, default is "pixel".
        """

        super().__init__(
            parent=parent,
            surface=surface,
            width=width,
            height=height,
            position=position,
            margin=margin,
            margin_unity=margin_unity,
            size_unity=size_unity,
            background_color=background_color,
        )
        self.children: list[UIElement] = []

    def add_child(self, child: UIElement):
        self.children.append(child)

    def remove_child(self, child: UIElement):
        if child in self.children:
            self.children.remove(child)
        else:
            raise ValueError("Child not found in container.")

    def draw(self):
        # Draw the container's background
        super().draw()

        # Draw all child elements
        for child in self.children:
            child.draw()

    def update(self):
        for child in self.children:
            child.update()
