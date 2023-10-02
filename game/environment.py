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
    def __init__(self, num_agents=2):
        self.river = River()
        self.orchard = Orchard()
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        # Let's initialize the river and orchard on the board
        for i in range(8):
            self.board[0][i] = "T"  # Orchard trees
            self.board[7][i] = "R"  # River

        self.agent_positions = {
            f"agent_{i+1}": np.array([0, 0]) for i in range(num_agents)
        }
        self.agent_rewards = {f"agent_{i+1}": 0 for i in range(num_agents)}

        # initialize the agents on the board
        for i in range(num_agents):
            # select a random spot on the board
            agent_pos = np.random.randint(0, 8, size=2)
            while self.board[agent_pos[0]][agent_pos[1]] not in [" ", "T", "R"]:
                agent_pos = np.random.randint(0, 8, size=2)
            self.board[agent_pos[0]][agent_pos[1]] = f"{i+1}"
            self.agent_positions[f"agent_{i+1}"] = agent_pos

    def _is_valid_move(self, new_pos):
        return 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8

    def step(self, agent_actions: dict = {}):
        # agent_actions is a dictionary of actions for each agent
        # agent_actions = {"agent_1": "move north", "agent_2": "clean river"}

        default_tile = [[" " for _ in range(8)] for _ in range(8)]
        default_tile[0] = ["T" for _ in range(8)]
        default_tile[7] = ["R" for _ in range(8)]

        # First, let's move the agents

        for agent, action in agent_actions.items():
            if action == "move north":
                new_pos = self.agent_positions[agent] + np.array([-1, 0])
            elif action == "move south":
                new_pos = self.agent_positions[agent] + np.array([1, 0])
            elif action == "move west":
                new_pos = self.agent_positions[agent] + np.array([0, -1])
            elif action == "move east":
                new_pos = self.agent_positions[agent] + np.array([0, 1])
            else:
                new_pos = self.agent_positions[agent]

            if self._is_valid_move(new_pos):
                # change the tile back to the default tile
                self.board[self.agent_positions[agent][0]][
                    self.agent_positions[agent][1]
                ] = default_tile[self.agent_positions[agent][0]][
                    self.agent_positions[agent][1]
                ]
                # update the agent position on the board with the agent number
                # just extract the number from the agent name
                self.board[new_pos[0]][new_pos[1]] = agent.split("_")[1]
                # update the agent position in the agent_positions dictionary
                self.agent_positions[agent] = new_pos

            # Now let's do the actions
            if action == "clean river":
                self.river.clean()
            elif action == "pick fruit":
                self.agent_rewards[agent] += self.orchard.pick_fruit()

        # Now let's update the board
        # First, let's reset the board
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        # Let's initialize the river and orchard on the board
        for i in range(8):
            self.board[7][i] = "R"
            self.board[0][i] = "T"

        # Now let's update the board with the agent positions
        for agent, pos in self.agent_positions.items():
            self.board[pos[0]][pos[1]] = agent.split("_")[1]

        self.orchard.grow_fruits(self.river.dirtiness)
        # make river 1 unit dirtier with 0.2 probability
        if self.river.dirtiness < 9 and np.random.rand() < 0.2:
            self.river.dirtiness += 1

    def display(self):
        # display the board with numbers on the rows and columns
        print("  ", end="")
        for i in range(8):
            print(i, end=" ")
        print()
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()

    def get_state(self):
        return {
            "agent_positions": self.agent_positions,
            "river_dirtiness": self.river.dirtiness,
            "orchard_fruits": self.orchard.fruits,
            "agent_rewards": self.agent_rewards,
            "board": self.board,
        }
