import json
from env.environment import CrisisEnv
from agent.agent import decide_action

def run_simulation():
    tasks = json.load(open("data/tasks.json"))
    env = CrisisEnv(tasks)

    obs = env.reset()
    done = False

    output = []

    while not done:
        action = decide_action(obs)
        obs, reward, done, _ = env.step(action)

        output.append(f"Action: {action} | Reward: {reward}")

    return "\n".join(output)


if __name__ == "__main__":
    print(run_simulation())