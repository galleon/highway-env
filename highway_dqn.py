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

env.close()
show_videos()




# // [
# //    [ 1.00000000e+00  1.00000000e+00  2.50000000e-01  3.33333334e-01 -2.32525110e-12]
# //    [ 1.00000000e+00  1.29051010e-01  2.50000000e-01  2.63392111e-02  2.29394281e-12]
# //    [ 1.00000000e+00  2.15129861e-01 -2.50000000e-01  1.22663571e-02  2.32724950e-12]
# //    [ 1.00000000e+00  4.04925321e-01  5.00000000e-01  2.38278257e-02  2.32525110e-12]
# //    [ 1.00000000e+00  4.91452144e-01 -3.14104298e-12  2.54022760e-02  2.32525110e-12]
# // ]