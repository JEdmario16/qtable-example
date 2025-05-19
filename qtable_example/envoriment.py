from qtable_example.agents.base_agent import BaseAgent
from qtable_example.internal.grid import Grid
from qtable_example.enums import Directions


class Envoriment:
    INVALID_ACTION_PENALTY = -100

    def __init__(
        self,
        grid: Grid,
        agent: BaseAgent,
        solution_position: tuple[int, int],
        max_steps: int = 1_000,
    ):
        self.grid = grid
        self.agent = agent
        self.agent_start_pos = (0, 0)
        self.agent_current_pos = self.agent_start_pos
        self.solution_position = solution_position
        self.done = False
        self.max_steps = max_steps
        self.current_step = 0
        self.episodes = 1000

    def step(self):
        """
        Execute an action in the environment.

        Args:
            action (int): The action to be executed.

        Returns:
            tuple: A tuple containing the next state, reward, and done flag.
        """
        valid_actions = [
            d
            for d, pos in self.grid.get_neighbors(self.agent_current_pos).items()
            if pos is not None
        ]

        # tecnicamente, é impossível não ter ações válidas, pela construção do grid
        assert len(valid_actions) > 0, "No valid actions available"

        action = self.agent.act(self.agent_current_pos, valid_actions)
        next_state = self.grid.get_position_following_direction(
            self.agent_current_pos, action, ignore_out_of_bounds=True
        )

        next_tile = self.grid.get_tile(next_state)
        if next_tile is None or next_tile.empty:
            reward = self.INVALID_ACTION_PENALTY
        else:
            reward = next_tile.reward

        # aprende
        self.agent.learn(
            state=self.agent_current_pos,
            action=action,
            reward=reward,
            next_state=next_state,
        )

        # Atualiza a posição do agente
        self.agent_current_pos = next_state
        self.done = self.agent_current_pos == self.solution_position

    def run(self):
        """
        Run the environment for a number of steps.
        """
        for _ in range(self.episodes):
            self.agent.reset()
            self.agent_current_pos = self.agent_start_pos
            self.done = False
            self.current_step = 0
            while not self.done and self.current_step < self.max_steps:
                self.step()
                self.current_step += 1

            if self.done:
                print("Agent reached the solution position!")
            else:
                print("Max steps reached without finding the solution.")


# exemplo
from qtable_example.agents.q_learng_agent import QLearningAgent
from qtable_example.internal.map_generator import MapGenerator

GRID_SIZE = (10, 10)  # in cells
TILE_SIZE = 64
GRID_START_POSITION = (0, 0)  # in pixels on the screen
SEED = 41  # seed for random generation
MAX_MAX_LENGTH = 100  # max length of the path
GAME_MAX_REWARD = 10.0  # max reward for the game
GAME_MIN_REWARD = -20  # min reward for the game
MAX_CELL_NEIGHBORS = 2  # max number of neighbors for each cell when generating the map
MAP_GENERATION_CREATE_SUBPATH_PROBABILITY = 0.9  # probability of creating a subpath


seed = 41

grid_size = (20, 20)
grid = Grid(grid_size=grid_size)
map_generator = MapGenerator(
    grid=grid,
    map_max_length=MAX_MAX_LENGTH,
    max_reward=GAME_MAX_REWARD,
    min_reward=GAME_MIN_REWARD,
    max_cell_neighbors=MAX_CELL_NEIGHBORS,
    map_generation_create_subpath_probability=MAP_GENERATION_CREATE_SUBPATH_PROBABILITY,
)

map_generator.generate_map(start_cell_position=(0, 0), seed=seed)
solution = grid.generate_random_solution(
    only_terminal=False,
)
map_generator.generate_euclidian_rewards(
    solution=solution,
)

agent = QLearningAgent(
    action_space=[Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT],
    state_space_dim=grid_size,
)

env = Envoriment(
    grid=grid, agent=agent, solution_position=solution.grid_position, max_steps=1000
)

env.run()
