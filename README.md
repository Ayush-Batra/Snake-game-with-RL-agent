*This repository contains the code for a reinforcement learning agent that learns to play the Snake game. The agent uses a Q-learning algorithm to learn the optimal actions to take in each state of the game.*

# File structure

**agent.py**: Contains the implementation of the agent. The agent is initialized with a Q-network (Linear_QNet) and a Q-trainer (QTrainer) that updates the network's weights based on the agent's experiences. The agent also has methods for getting the current state of the game, remembering experiences, and training both the short-term and long-term memory.

**gameai.py**: This is the implementation of the Snake game. The game has methods for moving the snake, checking for collisions, and updating the game state.

**model.py**: Contains the implementation of the Q-network, which is a simple linear model.

**helper.py**: Contains the method for plotting the agent's progress.

**snake.py**: Contains the snake game for human to play :)

# How to use
Run the agent.py file. 

This will initialize the agent and start training it by playing the Snake game.

The agent will play the game for a number of episodes, and the progress will be plotted using the helper plot function.

As the agent plays, it will learn the optimal actions to take in each state, and the plot will show the agent's progress in terms of the average score and the current score.

Once the agent reaches the desired level of performance, you can use the trained model to play the game.

# Note
This is a basic implementation of Q-learning agent for Snake game and thus the agent might not perform well or might not converge due to various reasons like Hyperparameter tuning, model architecture etc. 

Weights stored in ./model directory
