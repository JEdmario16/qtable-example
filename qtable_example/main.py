import pygame

from qtable_example.renders.camera_render import CameraGroup
from qtable_example.renders.grid_renderer import GridRenderer

from qtable_example.sprites.camera_center import CameraCenter
from qtable_example.sprites.tile_sprite import TileSprite

from qtable_example.internal.grid import Grid
from qtable_example.internal.map_generator import MapGenerator


# Settings
SCREEN_SIZE = (1920, 1080)
GRID_SIZE = (20, 20)  # in cells
TILE_SIZE = 64
GRID_START_POSITION = (0, 0)  # in pixels on the screen
SEED = 41  # seed for random generation
MAX_MAX_LENGTH = 100  # max length of the path

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Grid Renderer Example")
clock = pygame.time.Clock()
running = True

camera = CameraGroup()

grid = Grid(
    tile_size=TILE_SIZE,
    grid_size=GRID_SIZE,
)

map_generator = MapGenerator(
    grid=grid,
    map_max_length=MAX_MAX_LENGTH,
)

# WARNING: Map Generator will overwrite the grid
map_generator.generate_map(
    seed=SEED,
    start_cell_position=grid.get_grid_center(),
)

solution = grid.generate_random_solution(only_terminal=True)
map_generator.generate_euclidian_rewards(solution)

camera_center = CameraCenter(camera_group=camera)
grid_render = GridRenderer(
    grid=grid, grid_start_position=GRID_START_POSITION, camera_group=camera
)

grid_render._initialize_tiles()
grid_render.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            camera.zoom_scale += event.y * 0.03

    screen.fill((255, 255, 255))

    camera.update()
    camera.custom_draw(camera_center)

    pygame.display.update()
    clock.tick(60)
