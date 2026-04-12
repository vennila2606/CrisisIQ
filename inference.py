import sys
import os

# Force Python to include project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from openai import OpenAI
from env.environment import CrisisEnv

# ✅ Changed: reads from HF_TOKEN and API_BASE_URL instead of OPENAI_API_KEY
client = OpenAI(
    api_key=os.getenv("HF_TOKEN"),
    base_url=os.getenv("API_BASE_URL"),
)

# ✅ Changed: model is now read from env var instead of hardcoded
MODEL_NAME = os.getenv("MODEL_NAME")

def llm_decide_action(observation):
    prompt = f"""
You are a crisis intelligence agent. Given the situation below, choose ONE action:
VERIFY, ESCALATE_ALERT, IGNORE, REQUEST_MORE_INFO

Situation: {json.dumps(observation, indent=2)}

Respond with only the action.
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,  # ✅ Changed: was "gpt-4o-mini"
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_baseline():
    tasks = json.load(open("data/tasks.json"))
    env = CrisisEnv()
    total_score = 0

    print("[START]")  # ✅ Added: required by hackathon

    for i in range(2):
        obs = env.reset()
        done = False
        step_num = 0

        print(f"[STEP] task={i+1} status=started")  # ✅ Added

        while not done:
            action = llm_decide_action(obs)
            obs, reward, done, _ = env.step(action)
            total_score += reward
            step_num += 1

            # ✅ Added: required structured log format
            print(f"[STEP] task={i+1} step={step_num} action={action} reward={reward}")

    # ✅ Added: required by hackathon
    print(f"[END] total_score={total_score}")

if __name__ == "__main__":
    run_baseline()