import pytest
import numpy as np
import gymnasium
import gymnasium_env
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium_env.MazeWorldEnv import MazeWorldEnv

def test_maze_env_initialization():
    env = gymnasium.make('gymnasium_env/MazeWorldEnv-v0', render_mode="human")
    assert env is not None
    assert env.action_space.n == 4
    assert env.observation_space.shape == (2,)

def test_maze_env_reset():
    env = gymnasium.make('gymnasium_env/MazeWorldEnv-v0', render_mode="human")
    obs, info = env.reset()
    assert isinstance(obs, np.ndarray)
    assert obs.shape == (2,)
    assert isinstance(info, dict)
    assert "distance" in info

def test_maze_env_step():
    env = gymnasium.make('gymnasium_env/MazeWorldEnv-v0', render_mode="human")
    obs, _ = env.reset()
    

    new_obs, reward, terminated, truncated, info = env.step(0)  
    
    assert isinstance(new_obs, np.ndarray)
    assert new_obs.shape == (2,)
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)