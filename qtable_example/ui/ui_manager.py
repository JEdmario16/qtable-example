import pygame

from qtable_example.ui.container import Container
from qtable_example.ui.text_label import TextLabel
from qtable_example.enums import Unit, TextAlign
from typing import Literal

SizeModes = Literal["pixel", "percent"]


class UIManager:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self._elements = []

        main = Container(
            surface=self.screen,
            width=100,
            height=100,
            size_unity=Unit.PERCENT,
            position=(0, 0),
            background_color=(255, 255, 255),
        )

        header = Container(
            surface=self.screen,
            width=100,
            height=10,
            size_unity=Unit.PERCENT,
            position=(0, 0),
            background_color=(255, 255, 0),
        )

        print("Header created with size:", header.width, "x", header.height)

        text = TextLabel(
            parent=header,
            text="Algoritimos de RL para labirintos",
            font_size=32,
            font_color=(0, 0, 0),
            text_align_x=TextAlign.CENTER,
            text_align_y=TextAlign.CENTER,
        )
        header.add_child(text)

        model_selection_container = Container(
            parent=main,
            width=100,
            height=90,
            size_unity=Unit.PERCENT,
            position=(0, header.height),
            background_color=(255, 122, 122),
        )

        main.add_child(header)
        main.add_child(model_selection_container)
        self._elements.append(main)

    def draw(self):
        for element in self._elements:
            element.draw()

    def update(self):
        for element in self._elements:
            if hasattr(element, "update"):
                element.update()
