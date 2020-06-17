import gym
import highway_env
#from rl_agents.agents.common.factory import agent_factory
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
import sys
#from tqdm.notebook import trange
from utils import record_videos, show_videos, capture_intermediate_frames

env = gym.make("highway-v0")
obs, done = env.reset(), False

#model = DQN(MlpPolicy, env, verbose=1)
#model.learn(total_timesteps=25000)
#model.save("highway-deepq")

#del model # remove to demonstrate saving and loading

agent = DQN.load("highway-deepq")

env = record_videos(env)
obs, done = env.reset(), False
capture_intermediate_frames(env)

for step in range(env.unwrapped.config["duration"]):
    action, _states = agent.predict(obs)
    obs, rewards, dones, info = env.step(action)
    print(obs)
    print('-----------')

env.close()
show_videos()