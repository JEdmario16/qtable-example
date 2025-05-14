from qtable_example.internal.tile import Tile
from qtable_example.enums import Directions
from qtable_example.exceptions import OutOfBoundsError, AlreadyOccupiedError

import random


class Grid:
    """
    Representa o tabuleiro de um jogo, armazenando informações sobre as tiles (células) que o compõem.
    """

    DIRECTIONS_DELTA_MAP = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
        Directions.UP_LEFT: (-1, -1),
        Directions.UP_RIGHT: (-1, 1),
        Directions.DOWN_LEFT: (1, -1),
        Directions.DOWN_RIGHT: (1, 1),
    }

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

    def get_tile(self, position: tuple[int, int]) -> Tile:
        """
        Retorna a tile em uma posição específica.

        Args:
            position (tuple[int, int]): Posição no grid (linha, coluna).

        Returns:
            Tile: Tile na posição especificada.
        """
        return self._grid.get(position, None)

    def set_tile(self, position: tuple[int, int], tile: Tile):
        """
        Define uma tile em uma posição específica.

        Args:
            position (tuple[int, int]): Posição no grid (linha, coluna).
            tile (Tile): Tile a ser definida na posição especificada.
        """
        if not self.is_out_of_bounds(position):
            self._grid[position] = tile
        else:
            raise OutOfBoundsError(
                f"Position {position} is out of bounds for the grid size {self.grid_size}."
            )

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

    def is_terminal(self, position: tuple[int, int]) -> bool:
        """
        Verifica se uma posição é uma célula terminal.

        Args:
            position (tuple[int, int]): Posição no grid (linha, coluna).

        Returns:
            bool: True se a posição for uma célula terminal, False caso contrário.
        """
        neighbors = self.get_neighbors(position)
        return sum(1 for neighbor in neighbors.values() if neighbor is not None) == 1

    @property
    def terminal_cells(self) -> dict[tuple[int, int], Tile]:
        """
        Retorna um dicionário com as células terminais do grid.

        Returns:
            dict[tuple[int, int], Tile]: Dicionário com as células terminais.
        """
        return {
            position: tile
            for position, tile in self._grid.items()
            if self.is_terminal(position)
        }

    def generate_random_solution(self, only_terminal: bool = False) -> Tile:
        """
        Gera uma solução aleatória para o grid.
        """
        if only_terminal:
            solution = random.choice(list(self.terminal_cells.values()))
        else:
            solution = random.choice(list(self._grid.values()))
        solution.reward = self.max_reward
        solution.empty = False
        return solution
