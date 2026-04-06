from environment import CrisisEnv
from agent import decide_action

def evaluate():
    env = CrisisEnv()
    
    total_score = 0
    
    for _ in range(10):
        obs = env.reset()
        done = False
        steps = 0
        
        while not done:
            action = decide_action(obs)
            obs, reward, done, _ = env.step(action)
            total_score += reward
            steps += 1
    
    print("TOTAL SCORE:", total_score)
