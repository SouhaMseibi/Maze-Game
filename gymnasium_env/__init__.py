from gymnasium.envs.registration import register


register(
    id="gymnasium_env/MazeWorldEnv-v0",
    entry_point="gymnasium_env.envs:MazeWorldEnv",
)
    
print("Registered MazeWorldEnv-v0")