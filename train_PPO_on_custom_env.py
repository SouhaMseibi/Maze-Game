import gymnasium
import gymnasium_env
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO  # PPO often works better than A2C
from stable_baselines3.common.env_util import make_vec_env
from Board import Board

env = gymnasium.make('gymnasium_env/MazeWorldEnv-v0', render_mode="human")
check_env(env)


vec_env = make_vec_env('gymnasium_env/MazeWorldEnv-v0', n_envs=1)

print("Training model...")
model = PPO(
    "MlpPolicy", 
    vec_env, 
    verbose=1,
    learning_rate=0.0003,          # Slightly higher learning rate
    n_steps=2048,                  # More steps per update
    batch_size=64,                 # Smaller batch size for more frequent updates
    gamma=0.99,                    # Discount factor
    ent_coef=0.01,                 # Encourage exploration
    vf_coef=0.5,                   # Value function coefficient
    max_grad_norm=0.5,             # Clip gradient norm
    gae_lambda=0.95,               # GAE parameter
    clip_range=0.2   )              # PPO clip parameter

model.learn(total_timesteps=600000)
model.save("trained_maze_model_2")


print("Evaluating model...")
obs, _ = env.reset()
episode_reward = 0
episode_count = 0
max_episodes = 5
steps = 0
success_count = 0


for i in range(10000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    # env.render()

    episode_reward += reward
    steps += 1
    
    if terminated or truncated:
        episode_count += 1
        print(f"Episode {episode_count} finished after {steps} steps. Total reward: {episode_reward}")
        
        if terminated and not truncated:
            success_count += 1
            print("Goal reached successfully!")

        obs, _ = env.reset()
        episode_reward = 0
        steps = 0


print(f"Evaluation complete. Success rate: {success_count}/{max_episodes}")
env.close()
