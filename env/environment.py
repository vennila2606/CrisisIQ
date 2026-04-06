import json
import random

class CrisisEnv:
    def __init__(self):
        self.tasks = json.load(open("data/tasks.json"))
        self.current_task = None

    def reset(self):
        self.current_task = random.choice(self.tasks)
        return self.current_task["observation"]

    def step(self, action):
        correct = self.current_task["correct_action"]

        reward = 0
        done = False

        if action == correct:
            reward = 1
            done = True
        elif action == "VERIFY":
            reward = 0.5
        else:
            reward = -1

        return self.current_task["observation"], reward, done, {}
