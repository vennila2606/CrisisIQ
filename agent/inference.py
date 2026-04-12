from agent.agent import decide_action


def run_agent(env):
    observation = env.reset()
    done = False
    total_reward = 0
    step_count = 0

    while not done:
        action = decide_action(observation)

        print(f"Step {step_count + 1}")
        print("Observation:", observation)
        print("Action:", action)

        observation, reward, done, info = env.step(action)

        print("Reward:", reward)
        print("Done:", done)
        print("-" * 40)

        total_reward += reward
        step_count += 1

    return total_reward