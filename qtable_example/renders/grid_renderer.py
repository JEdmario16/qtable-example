import pygame

from qtable_example.internal.grid import Grid
from qtable_example.internal.tile import Tile
from qtable_example.sprites.tile_sprite import TileSprite


class GridRenderer(pygame.sprite.Group):

    EMPTY_TILE_COLOR = (0, 0, 0)  # Preto
    OCCUPIED_TILE_COLOR = (255, 0, 0)  # Vermelho

    def __init__(
        self,
        grid: Grid,
        grid_start_position: tuple[int, int] = (0, 0),
    ):
        """
        Inicializa o renderizador de grid.

        Args:
            grid (Grid): Instância do grid a ser renderizado.
        """
        super().__init__()
        self.grid = grid
        self.font = pygame.font.Font(None, 36)
        self.grid_start_position = grid_start_position
        self.tiles = {}
        self.tile_size = self.grid.tile_size

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

    def draw_grid_lines(self, surface: pygame.Surface):
        """
        Desenha as linhas do grid na superfície fornecida.

        Args:
            surface (pygame.Surface): Superfície onde o grid será desenhado.
        """

        width = self.grid.grid_size[1] * self.tile_size
        height = self.grid.grid_size[0] * self.tile_size
        start_x, start_y = self.grid_start_position

        line_color = (100, 100, 100)  # cinza escuro
        for row in range(self.grid.grid_size[0] + 1):
            y = start_y + row * self.tile_size
            pygame.draw.line(surface, line_color, (start_x, y), (start_x + width, y))

        for col in range(self.grid.grid_size[1] + 1):
            x = start_x + col * self.tile_size
            pygame.draw.line(surface, line_color, (x, start_y), (x, start_y + height))

    def reward_to_color(self, reward: float) -> tuple[int, int, int]:
        """
        Converte a recompensa em uma cor RGB.

        Args:
            max_reward (float): Recompensa máxima para normalização.

        Returns:
            tuple[int, int, int]: Cor RGB correspondente à recompensa.
        """
        if self.grid.max_reward == 0:
            return (0, 0, 0)

        t = max(0.0, min(reward / self.grid.max_reward, 1.0))
        r = int(255 * t)
        g = int(255 * (1 - t))
        b = int(255 * (1 - t))
        return (r, g, b)


import pygame

screen_size = (1920, 1080)
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Grid Renderer Example")
clock = pygame.time.Clock()
running = True
grid_render = GridRenderer(
    grid=Grid(tile_size=64, grid_size=(50, 50)),
    grid_start_position=(0, 0),
)

grid_render.grid.generate_random_map(max_length=30, seed=41)

grid_render._initialize_tiles()
grid_render.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    grid_render.draw(screen)
    grid_render.update()
    grid_render.draw_grid_lines(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
