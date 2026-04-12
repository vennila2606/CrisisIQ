import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

try:
    from openai import OpenAI
    from env.environment import CrisisEnv
except ImportError as e:
    print(json.dumps({"type": "[ERROR]", "message": f"Import failed: {str(e)}"}))
    sys.exit(1)

# ✅ Groq credentials via env vars
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
HF_TOKEN = os.getenv("HF_TOKEN", "")

try:
    client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)
except Exception as e:
    client = None


def rule_based_action(observation):
    """Fallback rule-based agent when LLM is unavailable."""
    confidence = observation.get("confidence_score", 0.5)
    severity = observation.get("severity_level", "low")
    reports = observation.get("related_reports", 0)

    if confidence < 0.2 and reports == 0:
        return "IGNORE"
    elif severity == "high" and reports >= 3:
        return "ESCALATE_ALERT"
    elif confidence > 0.7:
        return "ESCALATE_ALERT"
    elif reports >= 2:
        return "VERIFY"
    else:
        return "REQUEST_MORE_INFO"


def llm_decide_action(observation):
    """Try Groq LLM first, fall back to rule-based if it fails."""
    try:
        if not client or not HF_TOKEN:
            return rule_based_action(observation)

        prompt = f"""You are a crisis intelligence agent.
Given the situation below, choose ONE action: VERIFY, ESCALATE_ALERT, IGNORE, REQUEST_MORE_INFO

Situation:
{json.dumps(observation, indent=2)}

Respond with only the action word. Nothing else."""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        action = response.choices[0].message.content.strip().upper()
        if action not in ["VERIFY", "ESCALATE_ALERT", "IGNORE", "REQUEST_MORE_INFO"]:
            return rule_based_action(observation)
        return action
    except Exception:
        return rule_based_action(observation)


def run_baseline():
    try:
        tasks = json.load(open("data/tasks.json"))
        env = CrisisEnv(tasks)
        total_score = 0

        for i, task in enumerate(tasks):
            try:
                obs = env.reset()
                done = False
                step_num = 0

                print(json.dumps({
                    "type": "[START]",
                    "task_id": i + 1,
                    "headline": obs.get("headline", "")
                }))

                while not done:
                    action = llm_decide_action(obs)
                    obs, reward, done, _ = env.step(action)
                    total_score += reward
                    step_num += 1

                    print(json.dumps({
                        "type": "[STEP]",
                        "task_id": i + 1,
                        "step": step_num,
                        "action": action,
                        "reward": reward
                    }))

                print(json.dumps({
                    "type": "[END]",
                    "task_id": i + 1,
                    "total_reward": round(total_score, 2),
                    "done": True
                }))

            except Exception as e:
                print(json.dumps({
                    "type": "[ERROR]",
                    "task_id": i + 1,
                    "message": str(e)
                }))
                continue

        print(json.dumps({
            "type": "[SUMMARY]",
            "total_score": round(total_score, 2),
            "tasks_run": len(tasks)
        }))

    except Exception as e:
        print(json.dumps({"type": "[ERROR]", "message": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    run_baseline()





         
    