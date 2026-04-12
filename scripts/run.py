import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.environment import CrisisEnv
from agent.agent import decide_action
import json

# ✅ Load tasks
tasks = json.load(open("data/tasks.json"))

# ✅ Pass tasks to environment
env = CrisisEnv(tasks)

obs = env.reset()
done = False

print("Running one scenario...\n")

while not done:
    action = decide_action(obs)
    obs, reward, done, _ = env.step(action)

    print("Action:", action, "| Reward:", reward)