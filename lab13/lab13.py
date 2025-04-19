from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import gymnasium as gym
from types import MethodType

# TODO Write your reward functions here
def myreward(state):
    # Custom reward function
    pass

# Create environment

print("Creating environment...")
env = gym.make('FrozenLake-v1', render_mode='rgb_array', desc=None, map_name="4x4", is_slippery=False)

# Wrapper to modify the reward 
def transition_function(self, action):
    # perform and update
    state, reward, done, truncated, info = self.internal_step(action)
    reward = myreward(state) # TODO you can change this line to use your custom reward function
    return state, reward, done, truncated, info

# Transition function in gymnasium environments is called step
env.internal_step = env.step
env.step = MethodType(transition_function, env)


# Instantiate the agent
print("Creating agent...")
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./lab13/ppo_frozenlake_tensorboard/")
# Train the agent and display a progress bar
# TODO you may want to increase total_timesteps if your agent is not learning
model.learn(total_timesteps=int(1e4), progress_bar=True) 
# Save the agent
model.save("./lab13/ppo_frozenlake")
del model  # delete trained model to demonstrate loading

# Load the trained agent
# NOTE: if you have loading issue, you can pass `print_system_info=True`
# to compare the system on which the model was trained vs the current one
# model = DQN.load("dqn_lunar", env=env, print_system_info=True)
model = PPO.load("./lab13/ppo_frozenlake", env=env)

# Evaluate the agent
# NOTE: If you use wrappers with your environment that modify rewards,
#       this will be reflected here. To evaluate with original rewards,
#       wrap environment in a "Monitor" wrapper before other wrappers.
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
# Enjoy trained agent
vec_env = model.get_env()
obs = vec_env.reset()
for i in range(100):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render("human")