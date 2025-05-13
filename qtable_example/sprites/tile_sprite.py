import pygame
from qtable_example.internal.tile import Tile


class TileSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        tile: Tile,
        tile_color: tuple[int, int, int] = (0, 0, 0),
        font: pygame.font.Font | None = None,
        display_reward: bool = False,
        screen_coordinates: tuple[int, int] = (0, 0),
        max_reward: float = 10.0,
        camera_group: pygame.sprite.Group | None = None,
    ):
        super().__init__(camera_group)
        self.tile = tile
        self.font = font
        self.display_reward = display_reward
        self.image = pygame.Surface((tile.size, tile.size))
        self.rect = self.image.get_rect(topleft=screen_coordinates)
        self.tile_color = tile_color

        if not tile_color:
            self.tile_color = self.reward_to_color(tile.reward, max_reward)

    def update(self):
        self.image.fill(self.tile_color)
        if self.display_reward and self.tile.reward is not None:
            text_surface = self.font.render(
                str(round(self.tile.reward, 2)), True, (255, 255, 255)
            )
            text_rect = text_surface.get_rect(
                center=(self.tile.size // 2, self.tile.size // 2)
            )
            self.image.blit(text_surface, text_rect)

    def reward_to_color(self, reward: float, max_reward: float) -> tuple[int, int, int]:
        """
        Converte a recompensa em uma cor RGB.

        Args:
            max_reward (float): Recompensa máxima para normalização.

        Returns:
            tuple[int, int, int]: Cor RGB correspondente à recompensa.
        """
        if max_reward == 0:
            return (0, 0, 0)

        t = max(0.0, min(reward / max_reward, 1.0))
        r = int(255 * t)
        g = int(255 * (1 - t))
        b = int(255 * (1 - t))
        return (r, g, b)
