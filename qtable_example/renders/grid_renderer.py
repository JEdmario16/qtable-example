import pygame

from qtable_example.internal.grid import Grid
from qtable_example.sprites.tile_sprite import TileSprite
from qtable_example.renders.camera_render import CameraGroup


class GridRenderer(pygame.sprite.Group):

    EMPTY_TILE_COLOR = (64, 57, 64)  # Cinza escuro
    OCCUPIED_TILE_COLOR = (12, 183, 188)  # Azul claro

    def __init__(
        self,
        grid: Grid,
        camera_group: CameraGroup,
        grid_start_position: tuple[int, int] = (0, 0),
    ):
        """
        Inicializa o renderizador de grid.

        Args:
            grid (Grid): Instância do grid a ser renderizado.
            camera_group (CameraGroup): Grupo de câmera para renderização.
            grid_start_position (tuple[int, int]): Posição inicial do grid na tela.
        """
        super().__init__(camera_group)
        self.grid = grid
        self.font = pygame.font.Font(None, 36)
        self.grid_start_position = grid_start_position
        self.tiles = {}
        self.tile_size = self.grid.tile_size
        self.camera_group = camera_group
        self.grid_start_position = grid_start_position
        self._initialize_tiles()

    def update(self):
        """
        Atualiza o estado do renderizador.
        """
        for tile in self.sprites():
            tile.update()

    def _initialize_tiles(self):
        self.empty()
        for cell in self.grid._grid.values():
            tile = TileSprite(
                camera_group=self.camera_group,
                tile=cell,
                font=self.font,
                tile_color=(
                    self.EMPTY_TILE_COLOR
                    if cell.empty
                    else self.reward_to_color(cell.reward)
                ),
                display_reward=not cell.empty,
                screen_coordinates=self._grid_to_screen_coordinates(cell.grid_position),
            )
            self.add(tile)
            self.tiles[cell.grid_position[0], cell.grid_position[1]] = tile
        self.update()

    def _grid_to_screen_coordinates(
        self, grid_position: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Converte as coordenadas do grid para coordenadas da tela.

        Args:
            grid_position (tuple[int, int]): Posição no grid (linha, coluna).

        Returns:
            tuple[int, int]: Coordenadas na tela (x, y).
        """
        row, col = grid_position
        x = self.grid_start_position[0] + col * self.grid.tile_size
        y = self.grid_start_position[1] + row * self.grid.tile_size
        return x, y

    def interpolate_color(self, base_color, target_color, factor: float):
        """
        Interpola entre duas cores com base em um fator de 0.0 (cor base) a 1.0 (cor alvo).
        """
        return tuple(
            int(base + (target - base) * factor)
            for base, target in zip(base_color, target_color)
        )

    def reward_to_color(self, reward, min_reward=0, max_reward=10):
        """
        Retorna uma cor do gradiente vermelho → amarelo → verde
        com base no valor da recompensa.
        """
        # Normaliza a reward entre 0.0 e 1.0
        factor = (
            (reward - min_reward) / (max_reward - min_reward)
            if max_reward != min_reward
            else 0.5
        )
        factor = max(0.0, min(1.0, factor))  # clamp

        # Interpola entre vermelho (255,0,0) → amarelo (255,255,0) → verde (0,255,0)
        if factor < 0.5:
            # vermelho → amarelo
            r = 255
            g = int(255 * (factor / 0.5))
            b = 0
        else:
            # amarelo → verde
            r = int(255 * (1 - (factor - 0.5) / 0.5))
            g = 255
            b = 0

        return (r, g, b)


# import pygame

# screen_size = (1920, 1080)
# pygame.init()
# screen = pygame.display.set_mode(screen_size)
# pygame.display.set_caption("Grid Renderer Example")
# clock = pygame.time.Clock()
# running = True
# camera = CameraGroup()

# camera_center = CameraCenter(camera_group=camera)
# grid_render = GridRenderer(
#     grid=Grid(tile_size=64, grid_size=(50, 50)),
#     grid_start_position=(0, 0),
#     camera_group=camera
# )


# grid_render.grid.generate_random_map(max_length=100, seed=41)

# grid_render._initialize_tiles()
# grid_render.update()


# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # screen.fill((0, 0, 0))
#     # grid_render.draw(screen)
#     # grid_render.update()

#     screen.fill((255, 255, 255))

#     camera.update()
#     camera.custom_draw(camera_center)

#     pygame.display.update()
#     clock.tick(60)
# pygame.quit()
