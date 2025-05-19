from abc import ABC, abstractmethod

from typing import TypeVar, List, Tuple

T = TypeVar("T")


class BaseAgent(ABC):

    def __init__(self, action_space: List[T], state_space_dim: Tuple[int, int]):
        """
        Initialize the base agent.

        Args:
            action_space (list): The list of possible actions.
            state_space_dim (tuple[int, int]): The dimensions of the state space.
        """
        self.action_space = action_space
        self.state_space_dim = state_space_dim

    @abstractmethod
    def act(self, state: Tuple[int, int]) -> T:
        pass

    @abstractmethod
    def learn(
        self,
        state: Tuple[int, int],
        action: T,
        reward: float,
        next_state: Tuple[int, int],
    ):
        pass

    @abstractmethod
    def reset(self):
        pass
