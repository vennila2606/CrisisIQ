from env.environment import CrisisEnv
from agent import decide_action

env = CrisisEnv()

obs = env.reset()

done = False
total_reward = 0

while not done:
    action = decide_action(obs)
    print("ACTION:", action)
    
    obs, reward, done, _ = env.step(action)
    
    total_reward += reward

print("FINAL SCORE:", total_reward)
