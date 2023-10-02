from game.environment import GameEnvironment
from agents.gpt4_agent import GPT4Agent
import pandas as pd
import datetime

NUMBER_OF_STEPS = 200
API_KEY = "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"


def main(num_agents=2):
    env = GameEnvironment(num_agents=num_agents)

    agent_positions = env.agent_positions

    agents = {}

    for agent, pos in agent_positions.items():
        if agent == "agent_1":
            agents[agent] = GPT4Agent(
                agent_name=agent, api_key=API_KEY, pos=pos, agent_type="cooperative"
            )
        else:
            agents[agent] = GPT4Agent(
                agent_name=agent, api_key=API_KEY, pos=pos, agent_type="cooperative"
            )

    # For logging data
    log_data = {
        "step": [],
        "agent_actions": {f"agent_{i+1}": [] for i in range(num_agents)},
        "river_dirtiness": [],
        "orchard_fruits": [],
        "agent_rewards": {f"agent_{i+1}": [] for i in range(num_agents)},
    }

    for step in range(NUMBER_OF_STEPS):
        game_state = env.get_state()
        agent_actions = {}
        for agent in agents.values():
            agent_action = agent.make_decision(
                game_state
            )  # need to make a loop or something
            agent_actions[agent.agent_name] = agent_action

            log_data["agent_actions"][agent.agent_name].append(agent_action)

        env.step(agent_actions)  # need to pass a dictionary of actions

        # Log data for analysis
        log_data["step"].append(step)
        log_data["river_dirtiness"].append(env.river.dirtiness)
        log_data["orchard_fruits"].append(env.orchard.fruits)
        for agent_name in env.agent_rewards.keys():
            log_data["agent_rewards"][agent_name].append(env.agent_rewards[agent_name])

        # Optional: Display the game environment at each step
        print(f"Step: {step}")
        env.display()
        print(f"Agent actions: {agent_actions}")
        print("\n\n")

    # Now we will log the data to a CSV file
    # some of the data is nested so we need to flatten it
    # first we will flatten the agent_actions
    for agent, action in log_data["agent_actions"].items():
        log_data[f"{agent}_action"] = action
    # now we will flatten the agent_rewards
    for agent, reward in log_data["agent_rewards"].items():
        log_data[f"{agent}_reward"] = reward

    # now we will drop the original agent_actions and agent_rewards
    log_data.pop("agent_actions")
    log_data.pop("agent_rewards")

    # now we will convert the log_data dictionary to a pandas dataframe
    log_df = pd.DataFrame(log_data)

    # now we will save the dataframe to a csv file
    # we will use the current date and time to name the file
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    log_df.to_csv(f"game_logs/log_{date_time}.csv")


if __name__ == "__main__":
    main()
