from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import sys
import random

#sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app

from env.environment import CrisisEnv
from agent.agent import decide_action

app = FastAPI()

# Load tasks once at startup
base_dir = os.path.dirname(__file__)
tasks_path = os.path.join(base_dir, "data", "tasks.json")
with open(tasks_path, "r") as f:
    tasks = json.load(f)

env = CrisisEnv(tasks)
_state = {}
_current_obs = {}

class StepRequest(BaseModel):
    action: str

@app.get("/")
def home():
    return {"message": "Crisis Intelligence System Running 🚀"}

# ✅ POST /reset - required by hackathon
@app.post("/reset")
def reset():
    global _state, _current_obs
    obs = env.reset()
    _current_obs = obs
    _state = {
        "observation": obs,
        "done": False,
        "past_actions": [],
        "total_reward": 0
    }
    return {"observation": obs}

# ✅ POST /step - required by hackathon
@app.post("/step")
def step(request: StepRequest):
    global _state, _current_obs
    action = request.action
    obs, reward, done, info = env.step(action)

    _current_obs = obs
    _state["past_actions"].append({"action": action, "reward": reward})
    _state["total_reward"] = round(_state["total_reward"] + reward, 2)
    _state["done"] = done
    _state["observation"] = obs

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

# ✅ GET /state - required by hackathon
@app.get("/state")
def state():
    return _state

# ✅ Bonus /run endpoint
@app.get("/run")
def run_simulation():
    obs = env.reset()
    done = False
    steps_output = []
    total_reward = 0
    step_num = 1
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

