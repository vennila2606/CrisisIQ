import json
import random

headlines = [
    "Bridge collapse reported",
    "Flood warning issued",
    "Gas leak suspected",
    "Fake rumor spreading online",
    "Earthquake tremors detected",
    "Fire accident in warehouse",
    "Celebrity rumor causing panic",
    "Dam overflow warning",
    "Building crack reported",
    "Unverified explosion report"
]

sources = ["twitter", "news", "citizen", "gov_alert", "unknown"]

def generate_task(task_id):
    severity = random.choice(["low", "medium", "high"])
    confidence = round(random.uniform(0.1, 0.9), 2)
    reports = random.randint(0, 5)

    # Decide correct action logically
    if severity == "high" and reports >= 3:
        correct_action = "ESCALATE_ALERT"
    elif confidence < 0.3 and reports == 0:
        correct_action = "IGNORE"
    elif reports >= 1:
        correct_action = "VERIFY"
    else:
        correct_action = "REQUEST_MORE_INFO"

    return {
        "id": task_id,
        "difficulty": random.choice(["easy", "medium", "hard"]),
        "observation": {
            "headline": random.choice(headlines),
            "source": random.choice(sources),
            "confidence_score": confidence,
            "location": "India",
            "time_since_post": f"{random.randint(1, 20)} minutes",
            "related_reports": reports,
            "severity_level": severity
        },
        "correct_action": correct_action
    }

def generate_dataset(n=20):
    tasks = [generate_task(i) for i in range(1, n + 1)]

    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"{n} tasks generated successfully!")

if __name__ == "__main__":
    generate_dataset(20)
