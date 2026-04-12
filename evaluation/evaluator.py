import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from env.environment import CrisisEnv
from agent.agent import decide_action

def evaluate():
    base_dir = os.path.dirname(__file__)
    tasks_path = os.path.join(base_dir, "..", "data", "tasks.json")

    with open(tasks_path, "r") as f:
        tasks = json.load(f)

    # ✅ Pass tasks to CrisisEnv
    env = CrisisEnv(tasks)

    total_score = 0
    correct = 0

    for i in range(len(tasks)):
        obs = env.reset()
        done = False

        print(f"\n==============================")
        print(f"Task {i+1}")
        print(f"Headline: {obs.get('headline', 'Missing')}")
        print(f"Severity: {obs.get('severity_level', 'N/A')}")

        step_count = 0

        while not done:
            action = decide_action(obs)
            obs, reward, done, _ = env.step(action)

            print(f"Step {step_count+1} | Action: {action} | Reward: {reward}")

            if action == env.current_task["correct_action"]:
                correct += 1

            total_score += reward
            step_count += 1

    print(f"\n==============================")
    print(f"FINAL TOTAL SCORE: {round(total_score, 2)}")
    print(f"ACCURACY: {round(correct / len(tasks), 2)}")

if __name__ == "__main__":
    evaluate()