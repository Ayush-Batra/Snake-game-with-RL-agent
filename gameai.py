import pygame
from pygame.locals import *
import time
import random

pygame.init()

class SnakeGame():
    def __init__(self):
        self.screen = pygame.display.set_mode((600,600))
        self.fps = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        #init game state
        self.snake_position = [100,50]
        self.snake_body = [[100,50],
                        [90,50],
                        [80,50],
                        [70,50]
                    ]
            
        self.fruit_position = [random.randrange(1, (600//10)) * 10,
                        random.randrange(1, (600//10)) * 10]
        self.fruit_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

    def show_score(self,choice,color,font,size):
        score_font = pygame.font.SysFont(font,size)
        score_surface = score_font.render('Score:'+str(self.score),True,color)
        score_rect = score_surface.get_rect()
        self.screen.blit(score_surface,score_rect)

    # def game_over(self):
    #     my_font = pygame.font.SysFont('times new roman', 50)
    #     game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, (255,0,0))
    #     game_over_rect = game_over_surface.get_rect()
        
    #     game_over_rect.midtop = (200, 250)
        
    #     self.screen.blit(game_over_surface, game_over_rect)
    #     pygame.display.flip()

        
    def play_move(self,action):
        
        if action=='UP' and self.direction!='DOWN':
            self.direction = 'UP'
        if action =='DOWN' and self.direction!='UP':
            self.direction = 'DOWN'
        if action=='RIGHT' and self.direction!='LEFT':
            self.direction ='RIGHT'
        if action == 'LEFT' and self.direction!='RIGHT':
            self.direction = 'LEFT'
        
        if self.direction == 'UP':
            self.snake_position[1] -= 10
        if self.direction == 'DOWN':
            self.snake_position[1] += 10
        if self.direction == 'LEFT':
            self.snake_position[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_position[0] += 10
        
        self.snake_body.insert(0,list(self.snake_position))

    def update(self):
        self.screen.fill((255,255,255))
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, (0,255,0),
                            pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], 10, 10))
        self.show_score(1, (0,0,0), 'times new roman', 20)
        pygame.display.update()

    def collisition(self,head):
        if head[0] < 0 or head[0] > 590:
            return True
        if head[1] < 0 or head[1] > 590:
            return True
        for block in self.snake_body[1:]:
            if head[0] == block[0] and head[1] == block[1]:
                return True
        return False
    
    def play_step(self,move):
        
        if move.index(1) == 0:
            self.play_move('UP')
        elif move.index(1) == 1:
            self.play_move('DOWN')
        elif move.index(1) ==2:
            self.play_move('RIGHT')
        else:
            self.play_move('LEFT')
        
        reward = 0
        game_over = False
        if(self.collisition(self.snake_body[0])):
            game_over = True
            reward =- 10
            return reward, game_over,self.score

        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 10
            reward = 10
            self.fruit_spawn = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawn:
            self.fruit_position = [random.randrange(1, (600//10)) * 10,
                    random.randrange(1, (600//10)) * 10]
        self.fruit_spawn = True

        self.update()
        self.fps.tick(15)
        return reward,game_over,self.score

# dum = SnakeGame()
# while True:
#     dum.play_step()