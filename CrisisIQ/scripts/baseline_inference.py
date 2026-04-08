import sys
import os
# Force Python to include project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from openai import OpenAI
from env.environment import CrisisEnv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_decide_action(observation):
    prompt = f"""
You are a crisis intelligence agent.

Given the situation below, choose ONE action:
VERIFY, ESCALATE_ALERT, IGNORE, REQUEST_MORE_INFO

Situation:
{json.dumps(observation, indent=2)}

Respond with only the action.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def run_baseline():
    tasks = json.load(open("data/tasks.json"))
    env = CrisisEnv()

    total_score = 0

    for i in range(2):
        obs = env.reset()
        done = False

        print("\nTask", i + 1)

        while not done:
            action = llm_decide_action(obs)
            obs, reward, done, _ = env.step(action)

            print("LLM Action:", action, "| Reward:", reward)
            total_score += reward

    print("\nBaseline Score:", total_score)


if __name__ == "__main__":
    run_baseline()