"""import json
from env.environment import CrisisEnv
from agent.agent import decide_action

def run_simulation():
    tasks = json.load(open("data/tasks.json"))
    env = CrisisEnv()

    obs = env.reset()
    done = False

    output = []

    while not done:
        action = decide_action(obs)
        obs, reward, done, _ = env.step(action)

        output.append(f"Action: {action} | Reward: {reward}")

    return "\n".join(output)


if __name__ == "__main__":
    print(run_simulation())"""
"""import sys
import os
import json
import time

print("🔥 APP STARTED")

# ✅ Fix import path
sys.path.insert(0, os.path.abspath("."))

try:
    from env.environment import CrisisEnv
    from agent.agent import decide_action

    print("✅ Imports successful")

    # ✅ Safe path for Docker
    base_dir = os.path.dirname(__file__)
    tasks_path = os.path.join(base_dir, "data", "tasks.json")

    with open(tasks_path, "r") as f:
        tasks = json.load(f)

    print("✅ JSON loaded")

    env = CrisisEnv(tasks)

    obs = env.reset()
    done = False

    while not done:
        action = decide_action(obs)
        obs, reward, done, _ = env.step(action)
        print("Action:", action, "| Reward:", reward)

    print("✅ Simulation finished")

except Exception as e:
    print("❌ ERROR:", e)


# 🔥 KEEP CONTAINER ALIVE (VERY IMPORTANT)
print("🔄 Keeping container alive...")
while True:
    time.sleep(60)"""
from fastapi import FastAPI
import json
import os
import sys

# Fix imports
sys.path.insert(0, os.path.abspath("."))

from env.environment import CrisisEnv
from agent.agent import decide_action

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Crisis Intelligence System Running 🚀"}

@app.get("/state")
def state():
    return _state
    
@app.get("/run")
def run_simulation():
    base_dir = os.path.dirname(__file__)
    tasks_path = os.path.join(base_dir, "data", "tasks.json")

    with open(tasks_path, "r") as f:
        tasks = json.load(f)

    env = CrisisEnv(tasks)

    obs = env.reset()
    done = False

    steps_output = []
    total_reward = 0
    step_num = 1

    # Task name
    task_name = obs.get("headline", "Unknown Task")

    while not done:
        action = decide_action(obs)
        obs, reward, done, _ = env.step(action)

        steps_output.append({
            "step": step_num,
            "action": action,
            "reward": reward
        })

        total_reward += reward
        step_num += 1

    return {
        "task": task_name,
        "steps": steps_output,
        "total_reward": round(total_reward, 2)
    }