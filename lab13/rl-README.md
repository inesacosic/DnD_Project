# Reinforcement Learning

## Overview

RL is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize cumulative rewards. This lab demonstrates a Reinforcement Learning (RL) system using the OpenAI Gym for environment simulation, Stable Baselines3 for RL algorithms, and Matplotlib for visualization. 

## FrozenLake Environment

The FrozenLake environment is a classic RL problem where an agent must navigate a frozen lake to reach a goal while avoiding holes. The environment is represented as a grid, and the agent can move in four directions (left, right, up, down). The goal is to reach the goal state while avoiding falling into holes.

The state is represented as a single integer starting from 0 to 15 for 4x4 environment, where:
- 0: Starting point
- 15: Goal/Gift 

A simple reward function could be reward of 1 for reaching the goal state of 15 or 0 otherwise.

## Lab Instructions

For this lab you will have to understand the FrozenLake environment and stable-baselines3 library. You will have install the required dependencies. Some documentation links are provided below, but you may have to refer to more:

- https://gymnasium.farama.org/environments/toy_text/frozen_lake/
- https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
- https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html
- https://stable-baselines3.readthedocs.io/en/master/guide/tensorboard.html

You will find the plots of your runs in `./lab13/ppo_frozenlake/` directory. Refer to the links above  and other documentation to view and understand the plots. 

This lab covers Course Objective 2. 

## Lab Task

1. Write your custom reward function `myreward()` in `lab13.py` and observe the results. Try 3 different settings for the reward function and see how it affects the agent's learning. Make sure you run from the main directory so that `ppo_frozenlake` folder is created in the `lab13` directory.

2. Write a report in `lab13/lab13-report.md` and include the following:
   - A description of your custom reward function
   - A plot of the agent's learning curve of reward and episode length (note that episode is different from timestep) (You can use the tensorboard logs)
   - A discussion of how the reward function affected the agent's learning and behavior

3. Commit your code with the three different reward functions, your report and the `./lab13/ppo_frozenlake/` folder with the run data. Name your reward functions differntly, e.g., myreward1, myreward2, myreward3. Your final code may only be using one of the three reward functions, but you should have all three in your commit.