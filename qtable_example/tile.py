import pygame

import random

from qtable_example.exceptions import AlreadyOccupiedError, OutOfBoundsError


class TileSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        position: tuple[int, int],
        size: int,
        color: tuple[int, int, int],
        font,
        reward: float | None = None,
        display_reward: bool = False,
    ):
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
        if self.display_reward and self.reward is not None:
            text = self.font.render(str(self.reward), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.size // 2, self.size // 2))
            self.image.blit(text, text_rect)


class Tile:
    def __init__(
        self,
        position: tuple[int, int],
        size: int,
        color: str,
        reward: float | None = None,
        empty: bool = False,
    ):
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
                self._grid[(x, y)] = Tile(
                    position=(x, y),
                    size=tile_size,
                    color=(0, 0, 0),
                    reward=None,
                    empty=True,
                )

    def get_neighbors(
        self, position: tuple[int, int]
    ) -> dict[str, tuple[int, int] | None]:
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
        if cima_pos in self._grid and not self._grid[cima_pos].empty:
            neighbors["up"] = (x, y - self._grid[(x, y)].size)
        else:
            neighbors["up"] = None

        # Baixo
        baixo_pos = (x, y + self._grid[(x, y)].size)
        if baixo_pos in self._grid and not self._grid[baixo_pos].empty:
            neighbors["down"] = (x, y + self._grid[(x, y)].size)
        else:
            neighbors["down"] = None

        # Esquerda
        esquerda_pos = (x - self._grid[(x, y)].size, y)
        if esquerda_pos in self._grid and not self._grid[esquerda_pos].empty:
            neighbors["left"] = (x - self._grid[(x, y)].size, y)
        else:
            neighbors["left"] = None

        # Direita
        direita_pos = (x + self._grid[(x, y)].size, y)
        if direita_pos in self._grid and not self._grid[direita_pos].empty:
            neighbors["right"] = (x + self._grid[(x, y)].size, y)
        else:
            neighbors["right"] = None

        return neighbors

    def get_position_following_direction(
        self, tile: Tile, direction: str
    ) -> tuple[int, int]:
        directions = {
            "up": (0, -tile.size),
            "down": (0, tile.size),
            "left": (-tile.size, 0),
            "right": (tile.size, 0),
        }
        if direction in directions:
            return (
                tile.position[0] + directions[direction][0],
                tile.position[1] + directions[direction][1],
            )
        raise ValueError(
            f"Invalid direction: {direction}. Valid directions are: {list(directions.keys())}"
        )

    def add_on(self, tile: Tile, direction: str) -> Tile:
        assert tile.position in self._grid, "Tile position is out of grid bounds."

        new_position = self.get_position_following_direction(tile, direction)
        new_tile = Tile(new_position, tile.size, tile.color, tile.reward)

        if self.is_out_of_bounds(new_position):
            raise OutOfBoundsError(
                f"Desired position: {new_position} is out of grid bounds."
            )

        if self.is_occupied(new_position):
            raise AlreadyOccupiedError(
                f"Desired position: {new_position} is already occupied."
            )

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
    def __init__(
        self,
        grid: Grid,
        display: pygame.Surface,
        screen_size: tuple[int, int] = (800, 600),
        tile_size: int = 32,
    ):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.tiles = {}
        self.size = tile_size
        self.screen_size = screen_size
        self.grid = grid
        self.display = display
        self.generate_random_map(seed=41)

        self.update()

    def generate_random_map(
        self,
        comprimento_max: int = 100,
        start_tile_pos: tuple[int, int] | None = None,
        seed: int | None = None,
    ):
        COMPRIMENTO_MAX = 100
        comprimento = 0
        start_tile_position_x = self.screen_size[0] // self.size // 2
        start_tile_position_y = self.screen_size[1] // self.size // 2
        start_tile_position = (
            start_tile_position_x * self.size,
            start_tile_position_y * self.size,
        )

        start_tile = Tile(
            position=start_tile_position, size=self.size, color=(255, 213, 0), reward=10
        )
        self.grid[start_tile_position] = start_tile
        self.tiles[start_tile_position] = start_tile

        if seed is not None:
            random.seed(seed)
        else:
            random.seed(random.randint(0, 10000))

        self.generate_map_node(start_tile, 0, COMPRIMENTO_MAX)
        self.terminal_cells = self.terminal_cell_detection()

        for cell in self.terminal_cells:
            cell.color = (255, 0, 0)
            cell.reward = 1

        solution = random.choice(self.terminal_cells)
        solution.color = (0, 255, 0)
        self.generate_rewards(solution)

    def generate_map_node(
        self, from_tile: Tile, depth: int, max_depth: int, seed: int | None = None
    ):
        comprimento_maximo = max_depth - depth
        last_tile = from_tile

        while comprimento_maximo > 0:

            p = random.random()
            if p < 0.3:  # chance de gerar uma bifurcação
                self.generate_map_node(last_tile, depth + 1, max_depth)

            neighbors = self.grid.get_neighbors(last_tile.position)

            available_directions = [
                direction
                for direction, neighbor in neighbors.items()
                if neighbor is None
            ]

            # remove directions that are out of bounds
            available_directions = [
                direction
                for direction in available_directions
                if self.grid.get_position_following_direction(last_tile, direction)
                in self.grid
            ]

            print(f"Neighbors: {neighbors}")
            print(f"Available directions: {available_directions}")
            if not available_directions:
                print(f"No available directions from {last_tile.position}.")
                break
            try:
                # escolhe uma direção aleatória tal que a posição tenha menos que 1 vizinho
                # caso não seja possível, não gera mais tiles
                while available_directions:
                    direction = random.choice(available_directions)
                    available_directions.remove(direction)
                    neighbors = self.grid.get_neighbors(
                        self.grid.get_position_following_direction(last_tile, direction)
                    )
                    neighbors_count = sum(
                        1 for neighbor in neighbors.values() if neighbor is not None
                    )
                    if neighbors_count < 2:
                        break
                    direction = None
                if direction is None:
                    print(f"No valid direction found from {last_tile.position}.")
                    break

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

    def terminal_cell_detection(self):
        terminal_cells = []
        for cell in self.grid._grid.values():
            if not cell.empty:
                neighbors = self.grid.get_neighbors(cell.position)
                neighbors_count = sum(
                    1 for neighbor in neighbors.values() if neighbor is not None
                )
                if neighbors_count == 1:
                    terminal_cells.append(cell)
        return terminal_cells

    def generate_rewards(self, desired_solution: Tile):
        MAX_REWARD = 10
        assert (
            desired_solution.position in self.grid
        ), "Desired solution is out of grid bounds."

        for cell in self.grid._grid.values():
            if not cell.empty:
                distance = self.calculate_distance(cell, desired_solution)
                reward = (1 / distance) * MAX_REWARD if distance > 0 else MAX_REWARD
                cell.reward = round(reward, 2)

    def calculate_distance(self, tile: Tile, desired_solution: Tile) -> float:
        return (
            (tile.position[0] - desired_solution.position[0]) ** 2
            + (tile.position[1] - desired_solution.position[1]) ** 2
        ) ** 0.5

    def update(self):
        for cell in self.grid._grid.values():
            if cell is not None:
                tile = TileSprite(
                    position=cell.position,
                    size=cell.size,
                    color=cell.color,
                    reward=cell.reward,
                    font=self.font,
                    display_reward=not cell.empty,
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

screen_size = (1920, 1080)
g = Grid(tile_size=64, screen_size=screen_size)

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Tile Example")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
tile_renderer = TileRenderer(g, screen_size=screen_size, display=screen, tile_size=64)
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
    clock.tick(30)
pygame.quit()
