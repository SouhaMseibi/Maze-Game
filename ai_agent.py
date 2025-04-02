from enum import Enum
import numpy as np
import pygame
import os
import time
import gymnasium
import gymnasium_env
from gymnasium import spaces
from gymnasium.envs.registration import register
from stable_baselines3 import PPO 



env = gymnasium.make('gymnasium_env/MazeWorldEnv-v0', render_mode="human")

model = PPO.load("trained_maze_model", env=env)

vec_env = model.get_env()
obs = vec_env.reset()


total_reward = 0
steps = 0
max_steps = 50  
success = False

print("Testing trained agent...")

while steps < max_steps:

    action, _states = model.predict(obs, deterministic=True)

    obs, reward, terminated, truncated, info = env.step(action)
    
    total_reward += reward
    steps += 1
    
    print(f"Step {steps}: Action={action}, Reward={reward:.4f}, Distance={info['distance']:.2f}")

    env.render()
    
    time.sleep(0.1)
    
    if terminated:
        print(f"Goal reached after {steps} steps! Total reward: {total_reward:.2f}")
        success = True
        time.sleep(1)
        break
        
    if truncated:
        print(f"Episode truncated after {steps} steps. Total reward: {total_reward:.2f}")
        break


if not success and not truncated:
    print(f"Failed to reach goal within {max_steps} steps. Total reward: {total_reward:.2f}")

env.close()