import sys
import os
import json

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.environment import CrisisEnv
from agent.agent import decide_action


def evaluate():
    # ✅ Load tasks safely
    base_dir = os.path.dirname(__file__)
    tasks_path = os.path.join(base_dir, "..", "data", "tasks.json")

    with open(tasks_path, "r") as f:
        tasks = json.load(f)

    # ✅ Create environment
    env = CrisisEnv()

    total_score = 0
    correct = 0

    for i in range(len(tasks)):
        obs = env.reset()
        done = False

        print("\n==============================")
        print("Task", i + 1)
        print("Headline:", obs.get("headline", "Missing"))
        print("Source:", obs.get("source", "Unknown"))
        print("Confidence:", obs.get("confidence_score", "N/A"))
        print("Severity:", obs.get("severity_level", "N/A"))

        step_count = 0

        while not done:
            action = decide_action(obs)
            obs, reward, done, _ = env.step(action)

            print("Step", step_count + 1, "| Action:", action, "| Reward:", reward)

            # ✅ Count correct decisions
            if action == env.current_task["correct_action"]:
                correct += 1

            total_score += reward
            step_count += 1

    # ✅ Final results
    print("\n==============================")
    print("FINAL TOTAL SCORE:", round(total_score, 2))
    print("TOTAL STEPS:", correct)
    print("ACCURACY:", round(correct / len(tasks), 2))


if __name__ == "__main__":
    evaluate()
