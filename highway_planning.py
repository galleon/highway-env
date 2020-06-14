import gym
import highway_env
from rl_agents.agents.common.factory import agent_factory
import sys
#from tqdm.notebook import trange
from utils import record_videos, show_videos, capture_intermediate_frames

env = gym.make("highway-v0")
env = record_videos(env)
obs, done = env.reset(), False
capture_intermediate_frames(env)

# Make agent
agent_config = {
    "__class__": "<class 'rl_agents.agents.tree_search.deterministic.DeterministicPlannerAgent'>",
    "env_preprocessors": [{"method":"simplify"}],
    "budget": 50,
    "gamma": 0.7,
}
agent = agent_factory(env, agent_config)

# Run episode
# 
print(env.unwrapped.config["duration"])
for step in range(env.unwrapped.config["duration"]):
    action = agent.act(obs)
    obs, reward, done, info = env.step(action)

env.close()
show_videos()