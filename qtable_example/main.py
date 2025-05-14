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
GAME_MAX_REWARD = 10.0  # max reward for the game
GAME_MIN_REWARD = -200.0  # min reward for the game
MAX_CELL_NEIGHBORS = 2  # max number of neighbors for each cell when generating the map
MAP_GENERATION_CREATE_SUBPATH_PROBABILITY = 0.5  # probability of creating a subpath


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Grid Renderer Example")
clock = pygame.time.Clock()
running = True


game_surface_w = SCREEN_SIZE[0] * 0.7
game_surface_h = SCREEN_SIZE[1] * 1
game_surface = screen.subsurface(((0, 0, game_surface_w, game_surface_h)))

grid_size = (GRID_SIZE[0] * TILE_SIZE, GRID_SIZE[1] * TILE_SIZE)

camera = CameraGroup(game_surface)

grid = Grid(
    tile_size=TILE_SIZE,
    grid_size=GRID_SIZE,
    max_reward=GAME_MAX_REWARD,
)

map_generator = MapGenerator(
    grid=grid,
    map_max_length=MAX_MAX_LENGTH,
    max_reward=GAME_MAX_REWARD,
    min_reward=GAME_MIN_REWARD,
    max_cell_neighbors=MAX_CELL_NEIGHBORS,
    map_generation_create_subpath_probability=MAP_GENERATION_CREATE_SUBPATH_PROBABILITY,
)

# WARNING: Map Generator will overwrite the grid
map_generator.generate_map(
    # seed=SEED,
    start_cell_position=grid.get_grid_center(),
)

solution = grid.generate_random_solution(only_terminal=False)
map_generator.generate_euclidian_rewards(solution)

camera_center = CameraCenter(camera_group=camera)
grid_render = GridRenderer(
    grid=grid, grid_start_position=GRID_START_POSITION, camera_group=camera
)

grid_render._initialize_tiles()
grid_render.update()

MAX_ZOOM = 1.5
MIN_ZOOM = 0.5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            new_zoom = camera.zoom_scale + event.y * 0.03
            camera.zoom_scale = min(max(new_zoom, MIN_ZOOM), MAX_ZOOM)

    screen.fill((0, 0, 0))
    game_surface.fill((255, 255, 255))
    camera.update()
    camera.custom_draw(camera_center)

    pygame.display.update()
    clock.tick(30)
