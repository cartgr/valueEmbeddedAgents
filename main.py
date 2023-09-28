from game.environment import GameEnvironment
from agents.gpt4_agent import GPT4Agent
import pandas as pd
import datetime

NUMBER_OF_STEPS = 100
API_KEY = "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"  # Remember to set your API key here!


def main():
    env = GameEnvironment()
    agent = GPT4Agent(API_KEY)

    # For logging data
    log_data = {
        "step": [],
        "agent_action": [],
        "river_dirtiness": [],
        "orchard_fruits": [],
        "agent_reward": [],
    }

    for step in range(NUMBER_OF_STEPS):
        game_state = env.get_state()
        agent_action = agent.make_decision(game_state)
        env.step(agent_action)

        # Log data for analysis
        log_data["step"].append(step)
        log_data["agent_action"].append(agent_action)
        log_data["river_dirtiness"].append(game_state["river_dirtiness"])
        log_data["orchard_fruits"].append(game_state["orchard_fruits"])
        log_data["agent_reward"].append(game_state["agent_reward"])

        # Optional: Display the game environment at each step
        print(f"Step: {step}")
        print(f"Agent Action: {agent_action}")
        env.display()
        print("\n\n")

    # Now we will log the data to a CSV file

    df = pd.DataFrame(log_data)
    # log file name should be date and time
    log_file_name = "log_" + str(datetime.datetime.now()) + ".csv"
    df.to_csv("game_logs/" + log_file_name, index=False)


if __name__ == "__main__":
    main()
