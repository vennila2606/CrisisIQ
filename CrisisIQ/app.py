import sys
import os
import json

# ✅ Fix import path
sys.path.append(os.path.abspath("."))

from env.environment import CrisisEnv
from agent.agent import decide_action


def run_simulation():
    # ✅ Safe path for Docker
    base_dir = os.path.dirname(__file__)
    tasks_path = os.path.join(base_dir, "data", "tasks.json")

    with open(tasks_path, "r") as f:
        tasks = json.load(f)

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