class Tile:
    """
    Representa uma tile (ou célula) em um tabuleiro de jogo.
    Esta clase é utilizada para armazenar informações sobre a posição da tile, seu estado e facilitar
    a integração com o `Board`.

    """

    def __init__(
        self,
        grid_position: tuple[int, int],
        size: int = 32,
        empty: bool = True,
        reward: float = 0.0,
    ):
        """
        Inicializa uma nova instância de Tile.

        Args:
            grid_position (tuple[int, int]): Posição da tile no grid.
            size (int): Tamanho da tile (lado do quadrado).
            empty (bool): Indica se a tile está vazia ou ocupada.
            reward (float): Recompensa associada à tile.
        """
        self.grid_position = grid_position
        self.size = size
        self.empty = empty
        self.reward = reward

    def __repr__(self) -> str:
        return f"Tile(grid_position={self.grid_position}, size={self.size}, empty={self.empty}, reward={self.reward})"
