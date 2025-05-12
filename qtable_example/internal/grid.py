from qtable_example.internal.tile import Tile
from qtable_example.enums import Directions
from qtable_example.exceptions import OutOfBoundsError, AlreadyOccupiedError

import random


class Grid:
    """
    Representa o tabuleiro de um jogo, armazenando informações sobre as tiles (células) que o compõem.
    """

    DIRECTIONS_DELTA_MAP = {
        Directions.UP: (0, -1),
        Directions.DOWN: (0, 1),
        Directions.LEFT: (-1, 0),
        Directions.RIGHT: (1, 0),
        Directions.UP_LEFT: (-1, -1),
        Directions.UP_RIGHT: (1, -1),
        Directions.DOWN_LEFT: (-1, 1),
        Directions.DOWN_RIGHT: (1, 1),
    }

    MAP_GENERATION_CREATE_SUBPATH_PROBABILITY = (
        0.5  # Probabilidade de criar um subcaminho
    )

    def __init__(
        self,
        tile_size: int = 32,
        grid_size: tuple[int, int] = (10, 10),
        max_reward: float = 10.0,
    ):
        self.grid_size = grid_size
        self.tile_size = tile_size
        self._grid = self.generate_base_grid(tile_size)
        self.max_reward = max_reward

    def generate_random_map(
        self,
        max_length: int = 30,
        start_tile_position: tuple[int, int] = (0, 0),
        seed: int | None = None,
    ):
        """
        Gera um mapa aleatório com base em um ponto de partida e uma semente opcional.

        Args:
            max_length (int): Comprimento máximo do caminho.
            start_tile_position (tuple[int, int]): Posição inicial no grid.
            seed (int | None): Semente para geração aleatória.

        Returns:
            dict[tuple[int, int], Tile]: Mapa gerado.
        """
        if not start_tile_position:
            start_tile_position = self.get_grid_center()

        if seed is not None:
            random.seed(seed)
        else:
            random.seed(random.randint(0, 100))

        start_tile = Tile(
            grid_position=start_tile_position,
            size=self.tile_size,
            empty=False,
        )
        self._grid[start_tile_position] = start_tile

        self.generate_path(start_tile, max_length=max_length)

        # Gera recompensas para as tiles
        solution = self.choose_random_solution()
        self.generate_rewards(solution)

    def generate_path(
        self,
        start_tile: Tile,
        max_length: int = 30,
    ):
        """
        Gera um caminho aleatório a partir de uma tile inicial.

        Args:
            start_tile (Tile): Tile inicial.
            max_length (int): Comprimento máximo do caminho.

        Returns:
            dict[tuple[int, int], Tile]: Mapa gerado.
        """
        last_tile = start_tile
        current_length = 0

        while current_length < max_length:

            p = random.random()
            if p < self.MAP_GENERATION_CREATE_SUBPATH_PROBABILITY:
                self.generate_path(
                    start_tile=last_tile, max_length=max_length - current_length
                )

            available_directions = self._get_valid_directions(last_tile)

            if not available_directions:
                break

            # Tenta adicionar um tile de modo que a quanitdade de
            # tiles vizinhos seja < 2
            try:
                while available_directions:
                    direction = random.choice(available_directions)
                    available_directions.remove(direction)
                    neighbors = self.get_neighbors(
                        self.get_position_following_direction(
                            start_tile.grid_position, direction
                        ),
                        diagonal=False,
                    )

                    neighbors_count = sum(
                        1 for neighbor in neighbors.values() if neighbor is not None
                    )
                    if neighbors_count < 2:
                        break
                    direction = None
                if direction is None:
                    break

                new_tile = self.add_on(last_tile, direction)
                new_tile.reward = 1
                self._grid[new_tile.grid_position] = new_tile
                last_tile = new_tile
                current_length += 1

            except OutOfBoundsError:
                pass
            except AlreadyOccupiedError:
                pass
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def _get_valid_directions(
        self,
        tile: Tile,
    ):

        neighbors = self.get_neighbors(tile.grid_position, diagonal=False)

        # seleciona apenas as direções válidas (vazias) para adicionar uma nova tile
        valid_directions = [
            direction
            for direction, neighbor_cell in neighbors.items()
            if neighbor_cell is None
            and self.get_position_following_direction(
                position=tile.grid_position,
                direction=direction,
            )
            in self._grid
        ]
        return valid_directions

    def generate_base_grid(self, tile_size: int) -> dict[tuple[int, int], Tile]:
        grid = {}

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                grid[(row, col)] = Tile(
                    grid_position=(row, col),
                    size=tile_size,
                    empty=True,
                    reward=0.0,
                )

        return grid

    @property
    def non_empty_tiles(self) -> dict[tuple[int, int], Tile]:
        """
        Retorna um dicionário com as tiles não vazias do grid.

        Returns:
            dict[tuple[int, int], Tile]: Dicionário com as tiles não vazias.
        """
        return {
            position: tile for position, tile in self._grid.items() if not tile.empty
        }

    def get_position_following_direction(
        self,
        position: tuple[int, int],
        direction: Directions,
    ) -> tuple[int, int] | None:
        """
        Retorna a nova posição seguindo uma direção a partir de uma posição inicial.

        Args:
            position (tuple[int, int]): Posição inicial (linha, coluna).
            direction (Directions): Direção a seguir.

        Returns:
            tuple[int, int] | None: Nova posição (linha, coluna) ou None se fora dos limites.
        """
        row, col = position
        d_row, d_col = self.DIRECTIONS_DELTA_MAP[direction]
        new_pos = (row + d_row, col + d_col)

        if not self.is_out_of_bounds(new_pos):
            return new_pos
        return None

    def get_neighbors(
        self,
        position: tuple[int, int],
        diagonal: bool = False,
    ) -> dict[Directions, tuple[int, int] | None]:
        """
        Retorna os vizinhos de uma posição no grid.

        Args:
            position (tuple[int, int]): Posição no grid (linha, coluna).
            diagonal (bool): Se True, inclui vizinhos diagonais.

        Returns:
            dict[Directions, tuple[int, int] | None]: Dicionário com direções como chaves e posições dos vizinhos como valores.
        """
        row, col = position
        neighbors = {}

        directions = self.DIRECTIONS_DELTA_MAP.copy()
        if not diagonal:
            directions = {
                k: v
                for k, v in directions.items()
                if k
                not in (
                    Directions.UP_LEFT,
                    Directions.UP_RIGHT,
                    Directions.DOWN_LEFT,
                    Directions.DOWN_RIGHT,
                )
            }

        for direction, (d_row, d_col) in directions.items():
            new_pos = (row + d_row, col + d_col)
            if not self.is_out_of_bounds(new_pos) and not self.is_empty(new_pos):
                neighbors[direction] = new_pos
            else:
                neighbors[direction] = None

        return neighbors

    def add_on(self, tile: Tile, direction: Directions) -> Tile:
        """
        Adiciona uma tile seguindo uma direção a partir de uma posição inicial.

        Args:
            tile (Tile): Tile a ser adicionada.
            direction (Directions): Direção a seguir.

        Returns:
            Tile: Nova tile adicionada.
        """

        new_position = self.get_position_following_direction(
            tile.grid_position, direction
        )
        new_tile = Tile(
            grid_position=new_position,
            size=tile.size,
            empty=False,
            reward=tile.reward,
        )
        if self.is_out_of_bounds(new_position):
            raise OutOfBoundsError(
                f"Position {new_position} is out of bounds for the grid size {self.grid_size}."
            )

        if not self.is_empty(new_position):
            raise AlreadyOccupiedError(f"Position {new_position} is already occupied.")

        self._grid[new_position] = new_tile
        return new_tile

    def is_empty(self, position: tuple[int, int]) -> bool:
        """
        Verifica se uma posição no grid está vazia.

        Args:
            position (tuple[int, int]): Posição no grid (linha, coluna).

        Returns:
            bool: True se a posição estiver vazia, False caso contrário.
        """
        if not position in self._grid:
            raise OutOfBoundsError(
                f"Position {position} is out of bounds for the grid size {self.grid_size}."
            )
        return self._grid[position].empty

    def is_out_of_bounds(self, position: tuple[int, int]) -> bool:
        """
        Verifica se uma posição está fora dos limites do grid.

        Args:
            position (tuple[int, int]): Posição no grid (linha, coluna).

        Returns:
            bool: True se a posição estiver fora dos limites, False caso contrário.
        """
        return position not in self._grid

    def get_grid_center(self) -> tuple[int, int]:
        """
        Retorna o centro do grid.

        Returns:
            tuple[int, int]: Coordenadas do centro do grid (x, y).
        """
        return (self.grid_size[0] // 2, self.grid_size[1] // 2)

    def generate_rewards(self, desired_solution: Tile):

        for cell in self._grid.values():
            distance = self.calculate_distance(cell, desired_solution)
            reward = (
                (1 / distance) * self.max_reward if distance > 0 else self.max_reward
            )
            cell.reward = round(reward, 2)

    def terminal_cell_detection(self):
        terminal_cells = []
        for cell in self._grid.values():
            if not cell.empty:
                neighbors = self.get_neighbors(cell.grid_position, diagonal=False)
                neighbors_count = sum(
                    1 for neighbor in neighbors.values() if neighbor is not None
                )
                if neighbors_count == 1:
                    terminal_cells.append(cell)
        return terminal_cells

    def choose_random_solution(self) -> Tile:
        """
        Escolhe uma solução aleatória entre as tiles não vazias.

        Returns:
            Tile: Tile escolhida como solução.
        """
        terminal_cells = self.terminal_cell_detection()
        if not terminal_cells:
            raise ValueError("No terminal cells found in the grid.")
        return random.choice(terminal_cells)

    def calculate_distance(
        self,
        tile1: Tile,
        tile2: Tile,
    ) -> float:
        """
        Calcula a distância entre duas tiles.

        Args:
            tile1 (Tile): Primeira tile.
            tile2 (Tile): Segunda tile.

        Returns:
            float: Distância entre as duas tiles.
        """
        return (
            (tile1.grid_position[0] - tile2.grid_position[0]) ** 2
            + (tile1.grid_position[1] - tile2.grid_position[1]) ** 2
        ) ** 0.5
