from environment import CrisisEnv

env = CrisisEnv()

obs = env.reset()
print("OBS:", obs)

obs, reward, done, _ = env.step("VERIFY")
print("REWARD:", reward)
