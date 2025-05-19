from qtable_example.agents.base_agent import BaseAgent

import numpy as np

from typing import TypeVar

T = TypeVar("T")


class QLearningAgent(BaseAgent):

    def __init__(
        self,
        action_space: list[T],
        state_space_dim: tuple[int, int],
        *,
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        exploration_rate: float = 1.0,
        exploration_decay: float = 0.99,
        min_exploration_rate: float = 0.01,
    ):
        """
        Initialize the Q-learning agent.

        Args:
            learning_rate (float): The learning rate (alpha).
            discount_factor (float): The discount factor (gamma).
            exploration_rate (float): The initial exploration rate (epsilon).
            exploration_decay (float): The decay rate for exploration.
            min_exploration_rate (float): The minimum exploration rate.
            state_space_dim (tuple[int, int]): The dimensions of the state space.
        """

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.action_space = action_space

        # Initialize Q-table as a dictionary
        self.q_table = np.zeros((*state_space_dim, len(action_space)))

    def learn(self, state, action, reward, next_state):
        """
        Update the Q-value for the given state-action pair.

        Args:
            state (tuple): The current state.
            action (int): The action taken.
            reward (float): The reward received.
            next_state (tuple): The next state.
        """
        current_q_value = self.q_table[state[0], state[1], action.value]
        max_future_q_value = np.max(self.q_table[next_state[0], next_state[1], :])
        q_value_obs = reward + self.discount_factor * max_future_q_value
        td_error = q_value_obs - current_q_value
        new_q_value = current_q_value + self.learning_rate * td_error
        self.q_table[state[0], state[1], action.value] = new_q_value

        # Decay exploration rate
        self.exploration_rate = max(
            self.min_exploration_rate, self.exploration_rate * self.exploration_decay
        )

    def act(self, state: tuple, valid_moves: list[T]) -> T:
        """
        Choose an action based on the current state using epsilon-greedy policy.
        Args:
            state (tuple): The current state.
        Returns:
            T: The action to be taken.
        """

        if np.random.rand() < self.exploration_rate:
            # Explore: choose a random action
            return np.random.choice(valid_moves)
        else:
            # Exploit: choose the action with the highest Q-value
            q_values = self.q_table[*state]
            mapped_q_values = {
                action.value: q_values[action.value] for action in valid_moves
            }
            q_values = np.array(
                [mapped_q_values[action.value] for action in valid_moves]
            )
            max_q_value = np.max(q_values)
            best_actions = [
                action
                for action in valid_moves
                if mapped_q_values[action.value] == max_q_value
            ]
            return np.random.choice(best_actions)

    def reset(self):
        self.exploration_rate = 1.0
