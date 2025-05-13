import random
from qtable_example.internal.grid import Grid
from qtable_example.internal.tile import Tile
from qtable_example.enums import Directions


class MapGenerator:

    # Settings
    MAP_GENERATION_CREATE_SUBPATH_PROBABILITY = 0.5
    MAX_REWARD = 10.0
    MIN_REWARD = 0.0

    def __init__(self, grid: Grid, map_max_length: int = 100):
        self.grid = grid
        self.map_max_length = map_max_length

    def generate_map(self, start_cell_position: tuple[int, int], seed: int = 0) -> None:
        """
        Gera um mapa a partir de uma célula inicial.
        """

        assert (
            self.grid.get_tile(start_cell_position) is not None
        ), "Célula inicial não existe no grid."

        if seed:
            random.seed(seed)
        else:
            random.seed(random.randint(0, 1000))

        start_tile = self.grid.get_tile(start_cell_position)

        assert start_tile.empty, "Célula inicial não pode ser ocupada."

        start_tile.empty = False

        # Gera o caminho a partir da célula inicial
        self.generate_path(start_cell_tile=start_tile, max_length=self.map_max_length)

    def generate_path(
        self,
        start_cell_tile: Tile,
        max_length: int = 100,
    ):
        """
        Gera um caminho aleatório a partir de uma célula inicial.

        Args:
            start_cell_tile (Tile): Célula inicial a partir da qual o caminho será gerado.
            max_length (int): Comprimento máximo do caminho a ser gerado.

        Returns:
            None
        """

        last_tile = start_cell_tile
        current_length = 0
        while current_length < max_length:

            # verifica se deve criar um subcaminho
            p = random.random()
            if p < self.MAP_GENERATION_CREATE_SUBPATH_PROBABILITY:
                # cria um subcaminho
                self.generate_path(
                    start_cell_tile=last_tile, max_length=max_length - current_length
                )
            available_directions = self._get_valid_directions(last_tile)

            if not available_directions:
                # Se não houver direções disponíveis, termina o caminho
                break

            # tenta adicionar uma célula numa direção aleatória(válida)
            # tal que a quatidade de células vizinhas á ela seja menor que 2
            while available_directions:
                direction = random.choice(available_directions)
                available_directions.remove(direction)

                future_cell_pos = self.grid.get_position_following_direction(
                    position=last_tile.grid_position, direction=direction
                )
                neighbors = self.grid.get_neighbors(future_cell_pos, diagonal=False)

                if self._count_neighbors(neighbors) < 2:
                    break
                direction = None

            if direction is None:
                # Se não houver direções válidas, termina
                break
            new_tile = self.grid.add_on(last_tile, direction)
            last_tile = new_tile

    def _get_valid_directions(self, tile: Tile) -> list[Directions]:
        """
        Retorna as direções válidas a partir de uma célula.
        Uma direção é válida se:
        1. A célula vizinha não está ocupada
        2. A célula vizinha está dentro do mapa

        Args:
            tile (Tile): Célula a partir da qual as direções serão verificadas.
        Returns:
            list[Directions]: Lista de direções válidas.
        """
        neighbors = self.grid.get_neighbors(tile.grid_position, diagonal=False)

        valid_directions = [
            direction
            for direction, neighbor_cell_pos in neighbors.items()
            if neighbor_cell_pos is None
            and self.grid.get_position_following_direction(  # verifica se a posição está dentro do mapa
                position=tile.grid_position, direction=direction
            )
            in self.grid._grid
        ]

        return valid_directions

    def _count_neighbors(self, neighbors_dict: dict[Directions, Tile | None]) -> int:
        """
        Conta o número de vizinhos ocupados a partir de um dicionário de vizinhos.
        Args:
            neighbors_dict (dict[Directions, Tile | None]): Dicionário de vizinhos.
        Returns:
            int: Número de vizinhos ocupados.
        """
        return sum(1 for neighbor in neighbors_dict.values() if neighbor is not None)

    def calculate_distance(self, t1: Tile, t2: Tile) -> float:
        """
        Calcula a distância entre duas células.
        Para maior precisão, essa função irá considerar a distância euclidiana relativa á
        posição real da célula na tela(e não a posição no grid).

        Args:
            start (tuple[int, int]): Posição inicial.
            end (tuple[int, int]): Posição final.

        Returns:
            float: Distância entre as duas células.
        """
        x1 = t1.grid_position[0] * self.grid.tile_size
        y1 = t1.grid_position[1] * self.grid.tile_size
        x2 = t2.grid_position[0] * self.grid.tile_size
        y2 = t2.grid_position[1] * self.grid.tile_size
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def generate_euclidian_rewards(self, solution: Tile):
        """
        Gera recompensas euclidianas para as células do mapa.
        As recompensas são calculadas com base na distância da célula até a célula de solução,
        normalizadas pelo tamanho do mapa e pelo fator de recompensa máximo.
        As células que estão mais próximas da célula de solução terão recompensas mais altas,
        enquanto as células mais distantes terão recompensas mais baixas.
        As células que são terminais que não a solução terão uma punição negativa.

        Args:
            solution (Tile): Célula de solução.

        Returns:
            None
        """

        for tile in self.grid._grid.values():
            if tile.empty:
                continue

            if self.grid.is_terminal(tile.grid_position) and tile != solution:
                tile.reward = -self.MAX_REWARD
            elif tile != solution:
                distance = self.calculate_distance(tile, solution)
                grid_screen_size = self.grid.tile_size * self.grid.grid_size[0]
                normalized_distance = distance / grid_screen_size
                reward = (1 - normalized_distance) * self.MAX_REWARD
                tile.reward = max(0, min(reward, self.MAX_REWARD))
            else:
                tile.reward = self.MAX_REWARD
