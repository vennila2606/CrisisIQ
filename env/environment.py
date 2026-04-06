class CrisisEnv:
    def __init__(self, tasks):
        self.tasks = tasks
        self.current_task = None
        self.state_data = {}
        self.time_step = 0
