class CrisisEnv:
    def __init__(self, tasks):
        self.tasks = tasks
        self.current_task = None
        self.state_data = {}
        self.time_step = 0
        
   def reset(self):
    import random
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

    def step(self, action):
    reward = 0
    done = False
    
    correct_action = self.current_task["correct_action"]
    severity = self.current_task["observation"]["severity_level"]
    
    self.state_data["actions_taken"].append(action)
    self.time_step += 1
    self.state_data["time_elapsed"] += 1
    

    
    if action == correct_action:
        reward += 1
        
     
        if action == "ESCALATE_ALERT" and self.time_step <= 2:
            reward += 1.5
        
        done = True
    
    elif action == "VERIFY":
        reward += 0.5
        self.state_data["verified_sources"] += 1
    
    elif action == "REQUEST_MORE_INFO":
        reward += 0.3
    
    elif action == "IGNORE" and severity == "high":
        reward -= 2
        done = True
    
    else:
        reward -= 1
    
    
    if self.time_step >= 5:
        done = True
    
    return self._get_observation(), reward, done, {}

    def state(self):
    return self.state_data
    
    return obs
