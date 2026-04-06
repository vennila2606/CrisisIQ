import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.environment import CrisisEnv
from agent.agent import decide_action


def evaluate():
    import json

    # Load tasks
    tasks = json.load(open("data/tasks.json"))

    # Create environment
    env = CrisisEnv(tasks)

    total_score = 0

    for i in range(len(tasks)):
        obs = env.reset()
        done = False

        print("\n==============================")
        print("Task", i + 1)
        print("Headline:", obs.get("headline", "Missing"))
        print("Source:", obs.get("source"))
        print("Confidence:", obs.get("confidence_score"))
        print("Severity:", obs.get("severity_level"))

        while not done:
            action = decide_action(obs)
            obs, reward, done, _ = env.step(action)

            print("Action:", action, "| Reward:", reward)

            total_score += reward

    print("\n==============================")
    print("FINAL TOTAL SCORE:", total_score)


if __name__ == "__main__":
    evaluate()
