import torch
import numpy as np
import random
from collections import deque
from gameai import SnakeGame
from model import Linear_QNet, QTrainer
from helper import plot
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness control
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11,256,4)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)
        

    def get_state(self,snake):

        head = snake.snake_body[0]
        point_left = [head[0]-10,head[1]]
        point_right = [head[0]+10,head[1]]
        point_up = [head[0],head[1]-10]
        point_down = [head[0]-10,head[1]+10]
        dir_left = snake.direction == 'LEFT'
        dir_right = snake.direction == 'RIGHT'
        dir_up = snake.direction =='UP'
        dir_down = snake.direction == 'DOWN'

        state = [

            #danger straight
            (dir_right and snake.collisition(point_right)) or
            (dir_left and snake.collisition(point_left)) or
            (dir_up and snake.collisition(point_up)) or
            (dir_down and snake.collisition(point_down)),

            #danger right
            (dir_right and snake.collisition(point_down)) or
            (dir_left and snake.collisition(point_up)) or
            (dir_up and snake.collisition(point_right)) or
            (dir_down and snake.collisition(point_left)),

            #danger left
            (dir_right and snake.collisition(point_up)) or
            (dir_left and snake.collisition(point_down)) or
            (dir_up and snake.collisition(point_left)) or
            (dir_down and snake.collisition(point_right)),
            
            #move direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,

            #food location
            snake.fruit_position[0]<snake.snake_body[0][0], #food left
            snake.fruit_position[0]>snake.snake_body[0][0], #food right
            snake.fruit_position[1]<snake.snake_body[0][1], #food up
            snake.fruit_position[1]>snake.snake_body[0][1] #food down
        ]
        return np.array(state,dtype=int)

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def train_long_memory(self):
        if len(self.memory) >BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)


    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self,state):
        #exploration vs exploitation
        self.epsilon = 80 - self.n_games
        if(self.epsilon<0):
            if(self.n_games>200):
                self.epsilon = 0
            else:
                self.epsilon = 20
        final_move = [0,0,0,0]
        if random.randint(0,200)<self.epsilon:
            move = random.randint(0,3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state,dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    plot_scores = [] 
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        #get old state
        state_old = agent.get_state(game)
        #get move
        final_move = agent.get_action(state_old)
        #perform and get new state
        reward,done,score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old,final_move,reward,state_new,done)

        #remember
        agent.remember(state_old,final_move,reward,state_new,done)

        if done:
            #train long memory,plot 
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            print('Game',agent.n_games,score,'Record:',record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


    

if __name__ == '__main__':
    train()