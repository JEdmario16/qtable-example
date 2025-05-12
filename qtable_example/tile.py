import pygame

import random

class OutOfBoundsError(Exception):
    """Exception raised when a position is out of grid bounds."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AlreadyOccupiedError(Exception):
    """Exception raised when a position is already occupied."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TileSprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], size: int, color: tuple[int, int, int], font, reward: float | None = None, display_reward: bool = False):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=position)
        self.reward = reward
        self.color = color
        self.font = font
        self.display_reward = display_reward
        self.update()

    def update(self):   
        self.image.fill(self.color)
        if self.reward is not None and self.display_reward:
            text = self.font.render(str(self.reward), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.size // 2, self.size // 2))
            self.image.blit(text, text_rect)
        



class Tile:
    def __init__(self, position: tuple[int, int], size: int, color: str, reward: float | None = None, empty: bool = False):
        self.position = position
        self.size = size
        self.color = color
        self.reward = reward
        self.empty = empty

class Grid:
    def __init__(self, tile_size: int, screen_size: tuple[int, int]):
        self._grid: dict[tuple[int, int], Tile | None] = {}

        for x in range(0, screen_size[0], tile_size):
            for y in range(0, screen_size[1], tile_size):
                self._grid[(x, y)] = Tile(position=(x, y), size=tile_size, color=(0, 0, 0), reward=None, empty=True)


    def get_neighbors(self, position: tuple[int, int]) -> dict[str, tuple[int, int] | None]:
        """
        Obtem uma lista de vizinhos para a posição dada, nas direções: cima, baixo, esquerda, direita.\
        Excluindo vizinhos nas 'quinas' (ou seja NE, NW, SE, SW).
        Exemplo:

            | o | o |   |
            |   | x |   |
            |   | o |   |

            Resultaria em:
            {
                'up': (0, -32),
                'down': (0, 32),
                'left': (-32, 0),
                'right': (32, 0)
            }
        """

        x, y = position
        neighbors = {}

        # Cima
        cima_pos = (x, y - self._grid[(x, y)].size)
        if cima_pos in self._grid and self._grid[cima_pos].empty:
            neighbors['up'] = (x, y - self._grid[(x, y)].size)
        else:
            neighbors['up'] = None

        # Baixo
        baixo_pos = (x, y + self._grid[(x, y)].size)
        if baixo_pos in self._grid and self._grid[baixo_pos].empty:
            neighbors['down'] = (x, y + self._grid[(x, y)].size)
        else:
            neighbors['down'] = None
            
        # Esquerda
        esquerda_pos = (x - self._grid[(x, y)].size, y)
        if esquerda_pos in self._grid and self._grid[esquerda_pos].empty:
            neighbors['left'] = (x - self._grid[(x, y)].size, y)
        else:
            neighbors['left'] = None

        # Direita
        direita_pos = (x + self._grid[(x, y)].size, y)
        if direita_pos in self._grid and self._grid[direita_pos].empty:
            neighbors['right'] = (x + self._grid[(x, y)].size, y)
        else:
            neighbors['right'] = None

        return neighbors

    def get_position_following_direction(self, tile: Tile, direction: str) -> tuple[int, int]:
        directions = {
            'up': (0, -tile.size),
            'down': (0, tile.size),
            'left': (-tile.size, 0),
            'right': (tile.size, 0)
        }
        if direction in directions:
            return (
                tile.position[0] + directions[direction][0],
                tile.position[1] + directions[direction][1]
            )
        raise ValueError(f"Invalid direction: {direction}. Valid directions are: {list(directions.keys())}")


    def add_on(self, tile: Tile, direction: str) -> Tile:
        assert tile.position in self._grid, "Tile position is out of grid bounds."

        new_position = self.get_position_following_direction(tile, direction)
        new_tile = Tile(new_position, tile.size, tile.color, tile.reward)

        if self.is_out_of_bounds(new_position):
            raise OutOfBoundsError(f"Desired position: {new_position} is out of grid bounds.")

        if self.is_occupied(new_position):
            raise AlreadyOccupiedError(f"Desired position: {new_position} is already occupied.")

        self._grid[new_position] = new_tile
        return new_tile
    
    def is_out_of_bounds(self, position: tuple[int, int]) -> bool:
        return position not in self._grid
    
    def is_occupied(self, position: tuple[int, int]) -> bool:
        return position in self._grid and not self._grid[position].empty
        
    def __getitem__(self, item: tuple[int, int]) -> Tile | None:
        return self._grid.get(item, None)
    
    def __setitem__(self, key: tuple[int, int], value: Tile | None):
        if key in self._grid:
            self._grid[key] = value
        else:
            raise KeyError(f"Key {key} not found in grid.")

    def __contains__(self, item: tuple[int, int]) -> bool:
        return item in self._grid

class TileRenderer(pygame.sprite.Group):
    def __init__(self, grid: Grid, display: pygame.Surface, screen_size: tuple[int, int] = (800, 600)):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.tiles = {}
        self.size = 32
        self.screen_size = screen_size
        self.grid = grid
        self.display = display
        self.generate_random_map()

    def generate_random_map(self, comprimento_max: int = 100, start_tile_pos: tuple[int, int] | None = None):
        COMPRIMENTO_MAX = 400
        comprimento = 0
        start_tile_position_x = self.screen_size[0] // self.size // 2
        start_tile_position_y = self.screen_size[1] // self.size // 2
        start_tile_position = (start_tile_position_x * self.size, start_tile_position_y * self.size)

        start_tile = Tile(start_tile_position, self.size, (255, 213, 0), 0)
        self.grid[start_tile_position] = start_tile
        self.tiles[start_tile_position] = start_tile

        self.generate_map_node(start_tile, 0, COMPRIMENTO_MAX)

    def generate_map_node(self, from_tile: Tile, depth: int, max_depth: int):
        comprimento_maximo = max_depth - depth
        last_tile = from_tile

        while comprimento_maximo > 0:
            neighbors = self.grid.get_neighbors(last_tile.position)
            available_directions = [direction for direction, neighbor in neighbors.items() if neighbor is None]
            if not available_directions:
                break
            try:
                direction = random.choice(available_directions)
                new_tile = self.grid.add_on(last_tile, direction)
                new_tile.color = (255, 213, 0)
                new_tile.reward = 2
                self.grid[new_tile.position] = new_tile
                last_tile = new_tile
                comprimento_maximo -= 1
                
            except OutOfBoundsError:
                print(f"Out of bounds: {new_tile.position}")
            except AlreadyOccupiedError:
                print(f"Already occupied: {new_tile.position}")
    def update(self):
        for cell in self.grid._grid.values():
            if cell is not None:
                tile = TileSprite(
                    position=cell.position,
                    size=cell.size,
                    color=cell.color,
                    reward=cell.reward,
                    font=self.font,
                    display_reward=cell.empty
                )
                self.add(tile)
                self.tiles[cell.position] = tile

        for tile in self.sprites():
            tile.update()

# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Tile Example")
# clock = pygame.time.Clock()
# font = pygame.font.Font(None, 36)
# tile_renderer = TileRenderer(tree_max_depth=10)
# tile_renderer.generate_random_map()

# solution = random.choice(list(tile_renderer.tiles.values()))
# solution.reward = 1
# tile_renderer.update()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((0, 0, 0))
#     tile_renderer.draw(screen)
#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()

g = Grid(tile_size=32, screen_size=(800, 600))

# desenha um grid 3x3 a partir da posição (0, 0)
t1 = Tile(position=(0, 0), size=32, color='red', reward=0)
t2 = Tile(position=(32, 0), size=32, color='red', reward=0) # á direita de t1
t3 = Tile(position=(64, 0), size=32, color='red', reward=0) # á direita de t2
t4 = Tile(position=(0, 32), size=32, color='red', reward=0) # abaixo de t1
t5 = Tile(position=(32, 32), size=32, color='red', reward=0) # abaixo de t2
t6 = Tile(position=(64, 32), size=32, color='red', reward=0) # abaixo de t3
t7 = Tile(position=(0, 64), size=32, color='red', reward=0) # abaixo de t4
t8 = Tile(position=(32, 64), size=32, color='red', reward=0) # abaixo de t5
t9 = Tile(position=(64, 64), size=32, color='red', reward=0) # abaixo de t6

g[(0, 0)] = t1
g[(32, 0)] = t2
g[(64, 0)] = t3
g[(0, 32)] = t4
g[(32, 32)] = t5
g[(64, 32)] = t6
g[(0, 64)] = t7
g[(32, 64)] = t8
g[(64, 64)] = t9



print(g.get_neighbors((0, 0))) # [(0, -32), (0, 32), (-32, 0), (32, 0)]

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tile Example")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
tile_renderer = TileRenderer(g, screen_size=(800, 600), display=screen)
tile_renderer.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    tile_renderer.draw(screen)
    tile_renderer.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()