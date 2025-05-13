import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qtable_example.renders.grid_renderer import GridRenderer


class GUIRender:
    def __init__(self, screen: pygame.Surface, grid_render: GridRenderer):
        """
        Inicializa o renderizador GUI.

        Args:
            screen (pygame.Surface): Superfície da tela do Pygame.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.grid_render = grid_render

    def draw(self):
        """
        Desenha o grid e atualiza a tela.
        """
        self.screen.fill((255, 255, 255))
