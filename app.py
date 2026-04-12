''''from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, Union
import json
import os
import sys
sys.path.insert(0, os.path.abspath("."))
from env.environment import CrisisEnv
from agent.agent import decide_action
app = FastAPI()
base_dir = os.path.dirname(__file__)
tasks_path = os.path.join(base_dir, "data", "tasks.json")
with open(tasks_path, "r") as f:
    tasks = json.load(f)
env = CrisisEnv(tasks)
_state = {}
_current_obs = {}
class StepRequest(BaseModel):
    action: Union[str, dict]
class ResetRequest(BaseModel):
    task_id: Optional[int] = 1
def set_task(task_id: int = 1):
    task = next((t for t in tasks if t["id"] == task_id), tasks[0])
    env.current_task = task
    env.state_data = {
        "verified_sources": 0,
        "actions_taken": [],
        "time_elapsed": 0,
        "done": False
    }
    env.time_step = 0
    return env._get_observation()
@app.get("/")
def home():
    return {"message": "Crisis Intelligence System Running 🚀"}
@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "id": t["id"],
                "difficulty": t["difficulty"],
                "correct_action": t["correct_action"]
            }
            for t in tasks
        ]
    }
@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    global _state, _current_obs
    task_id = request.task_id if request and request.task_id else 1
    obs = set_task(task_id)
    _current_obs = obs
    _state = {
        "task_id": task_id,
        "observation": obs,
        "done": False,
        "past_actions": [],
        "total_reward": 0
    }
    return {"observation": obs, "task_id": task_id}
@app.get("/reset")
def reset_get(task_id: int = Query(default=1)):
    global _state, _current_obs
    obs = set_task(task_id)
    _current_obs = obs
    _state = {
        "task_id": task_id,
        "observation": obs,
        "done": False,
        "past_actions": [],
        "total_reward": 0
    }
    return {"observation": obs, "task_id": task_id}
@app.post("/step")
def step(request: StepRequest):
    global _state, _current_obs
    # ✅ Handle both {"action": "VERIFY"} and {"action": {"value": "VERIFY"}}
    if isinstance(request.action, dict):
        action = request.action.get("value", "VERIFY")
    else:
        action = request.action
    # ✅ Validate action
    valid_actions = ["VERIFY", "ESCALATE_ALERT", "IGNORE", "REQUEST_MORE_INFO"]
    if action not in valid_actions:
        action = "VERIFY"
    obs, reward, done, info = env.step(action)
    # ✅ Strictly between 0 and 1
    reward = max(0.001, min(0.999, round(float(reward), 3)))
    _current_obs = obs
    _state["past_actions"].append({"action": action, "reward": reward})
    _state["total_reward"] = round(_state["total_reward"] + reward, 3)
    _state["done"] = done
    _state["observation"] = obs
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }
@app.get("/state")
def state():
    return _state
@app.get("/run")
def run_simulation():
    results = []
    for task in tasks:
        obs = set_task(task["id"])
        done = False
        total_reward = 0
        step_num = 1
        while not done:
            action = decide_action(obs)
            obs, reward, done, _ = env.step(action)
            reward = max(0.001, min(0.999, round(float(reward), 3)))
            total_reward += reward
            step_num += 1
        results.append({
            "task_id": task["id"],
            "difficulty": task["difficulty"],
            "total_reward": round(total_reward, 3)
        })
    return {"results": results}
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
if __name__ == "__main__":
    main()'''

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from env.environment import CrisisEnv
from agent.agent import decide_action

app = FastAPI()

base_dir = os.path.dirname(__file__)
tasks_path = os.path.join(base_dir, "data", "tasks.json")
with open(tasks_path, "r") as f:
    tasks = json.load(f)

env = CrisisEnv(tasks)
_state = {}
_current_obs = {}

class StepRequest(BaseModel):
    action: str

class ResetRequest(BaseModel):
    task_id: Optional[int] = 1

def set_task(task_id: int = 1):
    task = next((t for t in tasks if t["id"] == task_id), tasks[0])
    env.current_task = task
    env.state_data = {
        "verified_sources": 0,
        "actions_taken": [],
        "time_elapsed": 0,
        "done": False
    }
    env.time_step = 0
    return env._get_observation()

@app.get("/")
def home():
    return {"message": "Crisis Intelligence System Running 🚀"}

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "id": t["id"],
                "difficulty": t["difficulty"],
                "correct_action": t["correct_action"]
            }
            for t in tasks
        ]
    }

# ✅ Handles POST /reset with OR without body
@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    global _state, _current_obs
    task_id = request.task_id if request and request.task_id else 1
    obs = set_task(task_id)
    _current_obs = obs
    _state = {
        "task_id": task_id,
        "observation": obs,
        "done": False,
        "past_actions": [],
        "total_reward": 0
    }
    return {"observation": obs, "task_id": task_id}

# ✅ Also handle GET /reset just in case
@app.get("/reset")
def reset_get(task_id: int = Query(default=1)):
    global _state, _current_obs
    obs = set_task(task_id)
    _current_obs = obs
    _state = {
        "task_id": task_id,
        "observation": obs,
        "done": False,
        "past_actions": [],
        "total_reward": 0
    }
    return {"observation": obs, "task_id": task_id}

@app.post("/step")
def step(request: StepRequest):
    global _state, _current_obs
    action = request.action
    obs, reward, done, info = env.step(action)
    reward = max(0.001, min(0.999, round(reward, 3)))
    _current_obs = obs
    _state["past_actions"].append({"action": action, "reward": reward})
    _state["total_reward"] = max(0.001, min(0.999, round(_state["total_reward"] + reward, 3)))
    _state["done"] = done
    _state["observation"] = obs
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return _state

@app.get("/run")
def run_simulation():
    results = []
    for task in tasks:
        obs = set_task(task["id"])
        done = False
        total_reward = 0
        step_num = 1
        while not done:
            action = decide_action(obs)
            obs, reward, done, _ = env.step(action)
            reward = max(0.001, min(0.999, round(reward, 3)))
            total_reward += reward
            step_num += 1
        results.append({
            "task_id": task["id"],
            "difficulty": task["difficulty"],
            "total_reward": round(total_reward, 2)
        })
    return {"results": results}
