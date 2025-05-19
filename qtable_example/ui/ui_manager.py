import pygame

from qtable_example.ui.container import Container
from qtable_example.ui.text_label import TextLabel

from typing import Literal

SizeModes = Literal["pixel", "percent"]


class UIManager:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self._elements = []

        container = Container(
            surface=self.screen,
            width=100,
            height=100,
            size_mode="percent",
            position=(0, 0),
            fill_color=(255, 255, 255),
            border_color=(0, 0, 0),
            alpha=1.0,
            border_width=2,
            border_radius=10,
            border_style="solid",
        )
        container.add_child(
            TextLabel(
                text="Exemplos de Modelos de Aprendizado por Reforço",
                font=pygame.font.Font(None, 28),
                padding=(10, 10, 10, 10),
                color=(0, 0, 0),
                align_text="center",
                parent_surface=container.image,
            )
        )

        self._elements.append(container)

    def draw(self):
        for element in self._elements:
            element.draw()
            element.update()
