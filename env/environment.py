import json
import random


class CrisisEnv:
    def __init__(self):
        try:
            with open("data/tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("❌ tasks.json not found in data/ folder")
        except json.JSONDecodeError:
            raise ValueError("❌ tasks.json is not valid JSON")

        self.current_task = None
        self.time_step = 0
        self.verified_count = 0

    def reset(self):
        if not self.tasks:
            raise ValueError("❌ No tasks available in dataset")

        self.current_task = random.choice(self.tasks)


        self.time_step = 0
        self.verified_count = 0

        return self.current_task["observation"]

    def step(self, action):
        if self.current_task is None:
            raise RuntimeError("❌ Call reset() before step()")

        correct = self.current_task.get("correct_action", None)
        severity = self.current_task["observation"].get("severity_level", "low")

        reward = 0
        done = False


        self.time_step += 1


        if action == correct:
            reward += 1


            if action == "ESCALATE_ALERT" and self.time_step <= 2:
                reward += 1.5

            done = True

        elif action == "VERIFY":
            reward += 0.5
            self.verified_count += 1

        elif action == "REQUEST_MORE_INFO":
            reward += 0.3

        elif action == "IGNORE":
            if severity == "high":
                reward -= 2  
                done = True
            else:
                reward += 0  

        else:
            reward -= 1 


        if self.time_step > 3:
            reward -= 0.5


        if self.time_step >= 5:
            done = True

        return self.current_task["observation"], reward, done, {
            "time_step": self.time_step,
            "verified_count": self.verified_count
        }

    def state(self):
        return {
            "time_step": self.time_step,
            "verified_count": self.verified_count,
            "current_task": self.current_task
        }
