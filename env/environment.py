"""from evaluation.grader import grade
import random


class CrisisEnv:
    def __init__(self, tasks):
        self.tasks = tasks
        self.current_task = None
        self.state_data = {}
        self.time_step = 0

    def reset(self):
        # Pick random task
        self.current_task = random.choice(self.tasks)

        # Reset state
        self.state_data = {
            "verified_sources": 0,
            "actions_taken": [],
            "time_elapsed": 0,
            "done": False
        }

        self.time_step = 0

        return self._get_observation()

    def _get_observation(self):
        obs = self.current_task["observation"].copy()

        # Add dynamic state info
        obs["verified_sources"] = self.state_data["verified_sources"]
        obs["time_elapsed"] = self.state_data["time_elapsed"]

        return obs

    def step(self, action):
        # Get correct action and severity
        correct_action = self.current_task["correct_action"]
        severity = self.current_task["observation"]["severity_level"]

        # Track action
        self.state_data["actions_taken"].append(action)

        # Update time
        self.time_step += 1
        self.state_data["time_elapsed"] += 1

        # ✅ Use grader (ONLY source of reward)
        reward = grade(
            action,
            correct_action,
            severity,
            self.time_step,
            self.state_data["verified_sources"]
        )

        # Update state for VERIFY
        if action == "VERIFY":
            self.state_data["verified_sources"] += 1

        # Done conditions
        done = False

        # If correct final decision → stop
        if action == correct_action:
            done = True

        # Limit steps
        if self.time_step >= 5:
            done = True

        # Save done state
        self.state_data["done"] = done

        return self._get_observation(), reward, done, {}

    def state(self):
        return self.state_data"""
"""import json
import random
from evaluation.grader import grade


class CrisisEnv:
    def __init__(self):
        with open("data/tasks.json", "r") as f:
            self.tasks = json.load(f)
        self.current_task = None
        self.state_data = {}
        self.time_step = 0

    def reset(self):
        # Pick random task
        self.current_task = random.choice(self.tasks)

        # Reset state
        self.state_data = {
            "verified_sources": 0,
            "actions_taken": [],
            "time_elapsed": 0,
            "done": False
        }

        self.time_step = 0

        return self._get_observation()

    def _get_observation(self):
        obs = self.current_task["observation"].copy()

        # Add dynamic state info
        obs["verified_sources"] = self.state_data["verified_sources"]
        obs["time_elapsed"] = self.state_data["time_elapsed"]

        return obs

    def step(self, action):
        # Get correct action and severity
        correct_action = self.current_task["correct_action"]
        severity = self.current_task["observation"]["severity_level"]

        # Track action
        self.state_data["actions_taken"].append(action)

        # Update time
        self.time_step += 1
        self.state_data["time_elapsed"] += 1

        # ✅ Use grader (ONLY source of reward)
        reward = grade(
            action,
            correct_action,
            severity,
            self.time_step,
            self.state_data["verified_sources"]
        )

        # Update state for VERIFY
        if action == "VERIFY":
            self.state_data["verified_sources"] += 1

        # Done conditions
        done = False

        # If correct final decision → stop
        if action == correct_action:
            done = True

        # Limit steps
        if self.time_step >= 5:
            done = True

        # Save done state
        self.state_data["done"] = done

        return self._get_observation(), reward, done, {}

    def state(self):
        return self.state_data"""
import random
from evaluation.grader import grade


class CrisisEnv:
    def __init__(self, tasks):   # ✅ FIX: accept tasks
        self.tasks = tasks
        self.current_task = None
        self.state_data = {}
        self.time_step = 0

    def reset(self):
        self.current_task = random.choice(self.tasks)

        self.state_data = {
            "verified_sources": 0,
            "actions_taken": [],
            "time_elapsed": 0,
            "done": False
        }

        self.time_step = 0
        return self._get_observation()

    def _get_observation(self):
        obs = self.current_task["observation"].copy()
        obs["verified_sources"] = self.state_data["verified_sources"]
        obs["time_elapsed"] = self.state_data["time_elapsed"]
        return obs

    def step(self, action):
        correct_action = self.current_task["correct_action"]
        severity = self.current_task["observation"]["severity_level"]

        self.state_data["actions_taken"].append(action)

        self.time_step += 1
        self.state_data["time_elapsed"] += 1

        # ✅ Reward from grader
        reward = grade(
            action,
            correct_action,
            severity,
            self.time_step,
            self.state_data["verified_sources"]
        )

        if action == "VERIFY":
            self.state_data["verified_sources"] += 1

        done = False

        if action == correct_action:
            done = True

        if self.time_step >= 5:
            done = True

        self.state_data["done"] = done

        return self._get_observation(), reward, done, {}

    def state(self):
        return self.state_data