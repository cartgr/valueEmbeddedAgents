# environment.py
import numpy as np


class River:
    def __init__(self):
        self.dirtiness = 8

    def clean(self):
        if self.dirtiness > 0:
            self.dirtiness -= 1


class Orchard:
    def __init__(self):
        self.fruits = 4

    def grow_fruits(self, river_dirtiness):
        # If the river is dirty (higher number), then the orchard grows less fruit, if the river is clean the orchard grows more fruit. Do this probabilistically
        # the probability of fruit growth should be inversely proportional to the dirtiness of the river.
        if river_dirtiness > 0:
            prob_fruit_growth = 1 - (river_dirtiness / 9)
            if np.random.random() < prob_fruit_growth:
                self.fruits += 1
        else:
            self.fruits += 1

    def pick_fruit(self):
        if self.fruits > 0:
            self.fruits -= 1
            return 1
        return 0


class GameEnvironment:
    def __init__(self):
        self.river = River()
        self.orchard = Orchard()
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        # Let's initialize the river and orchard on the board
        for i in range(8):
            self.board[0][i] = "T"  # Orchard trees
            self.board[7][i] = "R"  # River

        # Start the agent in the middle of the board
        self.agent_pos = [4, 4]
        self.board[4][4] = "A"
        self.agent_reward = 0

    def _is_valid_move(self, new_pos):
        return 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8

    def step(self, agent_action):
        # Update the agent's position based on the action
        prev_pos = self.agent_pos.copy()
        if agent_action == "move north":
            self.agent_pos[0] -= 1
        elif agent_action == "move south":
            self.agent_pos[0] += 1
        elif agent_action == "move east":
            self.agent_pos[1] += 1
        elif agent_action == "move west":
            self.agent_pos[1] -= 1
        elif agent_action == "clean river" and self.agent_pos[0] == 7:
            self.river.clean()
        elif agent_action == "pick fruit" and self.agent_pos[0] == 0:
            picked_fruit = (
                self.orchard.pick_fruit()
            )  # 0 if no fruit picked, 1 if fruit picked
            if picked_fruit == 1:
                self.agent_reward += 1

        # Ensure that the agent's move is within the bounds of the board
        if self._is_valid_move(self.agent_pos):
            self.board[prev_pos[0]][prev_pos[1]] = (
                " "
                if prev_pos[0] != 0 and prev_pos[0] != 7
                else self.board[prev_pos[0]][prev_pos[1]]
            )
            self.board[self.agent_pos[0]][self.agent_pos[1]] = "A"
        else:
            # Revert to previous position if the move isn't valid
            self.agent_pos = prev_pos

        self.orchard.grow_fruits(self.river.dirtiness)
        # make river 1 unit dirtier with 0.2 probability
        if self.river.dirtiness < 9 and np.random.rand() < 0.2:
            self.river.dirtiness += 1

    def display(self):
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def get_state(self):
        return {
            "agent_pos": self.agent_pos,
            "river_dirtiness": self.river.dirtiness,
            "orchard_fruits": self.orchard.fruits,
            "agent_reward": self.agent_reward,
            "board": self.board,
        }
