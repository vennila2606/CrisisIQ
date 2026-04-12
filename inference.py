import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai import OpenAI
from env.environment import CrisisEnv

# ✅ Validate env vars before starting
HF_TOKEN = os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not HF_TOKEN:
    raise EnvironmentError("HF_TOKEN is not set")
if not API_BASE_URL:
    raise EnvironmentError("API_BASE_URL is not set")
if not MODEL_NAME:
    raise EnvironmentError("MODEL_NAME is not set")

client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL,
)

def llm_decide_action(observation):
    prompt = f"""
You are a crisis intelligence agent. Given the situation below, choose ONE action:
VERIFY, ESCALATE_ALERT, IGNORE, REQUEST_MORE_INFO

Situation: {json.dumps(observation, indent=2)}

Respond with only the action word, nothing else.
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        action = response.choices[0].message.content.strip()
        # ✅ Validate response is one of the allowed actions
        valid_actions = ["VERIFY", "ESCALATE_ALERT", "IGNORE", "REQUEST_MORE_INFO"]
        if action not in valid_actions:
            action = "VERIFY"  # fallback
        return action
    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        return "VERIFY"  # fallback so simulation doesn't crash

def run_baseline():
    tasks_path = os.path.join(os.path.dirname(__file__), "data", "tasks.json")
    with open(tasks_path, "r") as f:
        tasks = json.load(f)

    env = CrisisEnv(tasks)
    total_score = 0

    print("[START]")

    for i in range(2):
        obs = env.reset()
        done = False
        step_num = 0

        print(f"[STEP] task={i+1} status=started")

        while not done:
            try:
                action = llm_decide_action(obs)
            except Exception as e:
                print(f"❌ Action decision failed: {e}")
                action = "VERIFY"

            obs, reward, done, _ = env.step(action)
            total_score += reward
            step_num += 1

            print(f"[STEP] task={i+1} step={step_num} action={action} reward={reward}")

    print(f"[END] total_score={total_score}")

if __name__ == "__main__":
    run_baseline()