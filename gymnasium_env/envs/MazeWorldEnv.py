import numpy as np
import pygame
from enum import Enum
import gymnasium as gym
from gymnasium import spaces
from Board import Board



class MazeWorldEnv(gym.Env):

    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 6}
    size = 64 #Ghost pixel size 


    def __init__(self, render_mode="human", size=size):

        self.maze = Board

        self.size = size  
        self.window_size = size * len(self.maze[0])      

        self.goal_position = None
        self.initial_position = (1, 1) # (j ,i )  (x,y)

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 2:
                    self.goal_position = (j, i)
                if self.goal_position is not None and self.initial_position is not None:
                    break
        
        

        self._agent_location = np.array(self.initial_position, dtype=int)  
        self._target_location = np.array(self.goal_position, dtype=int) 
        self.observation_space = spaces.Box(low=0, high= len(self.maze[0]) - 1, shape=(2,), dtype=np.int32)
        self.action_space = spaces.Discrete(4)
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None
        self.show_goal_message = False

        self.agent_img = None
        self.target_img= None 

        self.max_steps = 1000
        self.current_steps = 0


    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }


    def reset(self , seed=None, options=None):

        super().reset(seed=seed)
        
        self._agent_location = np.array(self.initial_position, dtype=int)
        self._target_location = np.array(self.goal_position, dtype=int)
        self.show_goal_message = False
        self.current_steps = 0

        observation = np.array(self._agent_location, dtype=np.int32)
        info = self._get_info()

        return observation, info


    def step(self, action): 

        prev_location = np.copy(self._agent_location)
        self.current_steps += 1

        if action == self.LEFT:
            self._agent_location[0] -= 1
        elif action == self.RIGHT:
            self._agent_location[0] += 1
        elif action == self.UP:
            self._agent_location[1] -= 1
        elif action == self.DOWN:
            self._agent_location[1] += 1


        if (0 <= self._agent_location[0] < len(self.maze[0]) and 
            0 <= self._agent_location[1] < len(self.maze[0]) and 
            self.maze[self._agent_location[1]][self._agent_location[0]] != 1) :
               
                pass 

        else :
            
            self._agent_location = prev_location


        terminated = np.array_equal(self._agent_location, self._target_location)
        truncated = self.current_steps >= self.max_steps

        if terminated:
            reward = 10.0  
            self.show_goal_message = True
        elif truncated:
            reward = -5.0
        else:
            reward = -0.01

            maze_size = max(len(self.maze), len(self.maze[0]))
            prev_distance = np.linalg.norm(prev_location - self._target_location)
            new_distance = np.linalg.norm(self._agent_location - self._target_location)

            reward += 0.5 * (prev_distance - new_distance) / maze_size

        
        observation = np.array(self._agent_location, dtype=np.int32)
        info = self._get_info()

        return observation, reward, terminated, truncated, info


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()



    def render(self):
        if self.render_mode == "human":
            if self.window is None:
                pygame.init()
                pygame.display.init()
                self.window = pygame.display.set_mode((self.window_size, self.window_size))
            if self.clock is None:
                self.clock = pygame.time.Clock()

            if not hasattr(self, 'agent_img') or self.agent_img is None:
                # self.agent_img = pygame.image.load("/home/souha/maze_game/images/ghost.png").convert_alpha()
                self.agent_img = pygame.image.load("./images/ghost.png").convert_alpha()    #PATH INSIDE DOCKER CONTAINER 
            if not hasattr(self, 'target_img') or self.target_img is None:
                # self.target_img = pygame.image.load("/home/souha/maze_game/images/home.png").convert_alpha()
                self.target_img = pygame.image.load("./images/home.png").convert_alpha()
               
            
            
            COLORS = {
                0: (200, 200, 200), 
                1: (100, 100, 100)  
            }
            
            canvas = pygame.Surface((self.window_size, self.window_size))
            canvas.fill((0, 0, 0))  
            

            for i in range(len(self.maze)):
                for j in range(len(self.maze[i])):
                    
                    x = j * self.size
                    y = i * self.size
                    
                    cell_type = self.maze[i][j]
                    
                    if cell_type == 2:  
                       
                        rect = pygame.Rect(x, y, self.size, self.size)
                        pygame.draw.rect(canvas, (200, 200, 200), rect)  
                        pygame.draw.rect(canvas, (50, 50, 50), rect, 1)  # Border
                        canvas.blit(self.target_img, (x, y))
                   
                    else:  
                        rect = pygame.Rect(x, y, self.size, self.size)
                        pygame.draw.rect(canvas, COLORS[cell_type], rect)
                        pygame.draw.rect(canvas, (50, 50, 50), rect, 1)  
            

            canvas.blit(
                self.agent_img,
                (self._agent_location[0] * self.size ,
                 self._agent_location[1] * self.size )
            )
            
            
            if self.show_goal_message:
                
                message = "GOAL REACHED!"
                
                font = pygame.font.SysFont(None, 36)
                text = font.render(message, True, (255, 255, 0))
                text_rect = text.get_rect(center=(self.window_size // 2, self.window_size // 2))
                
               
                msg_width = max(text.get_width() + 40, 160)
                msg_height = text.get_height() + 20
                
                
                msg_box = pygame.Rect(
                    (self.window_size - msg_width) // 2,
                    (self.window_size - msg_height) // 2,
                    msg_width,
                    msg_height
                )
                s = pygame.Surface((msg_box.width, msg_box.height), pygame.SRCALPHA)
                s.fill((0, 0, 0, 180)) 
                canvas.blit(s, (msg_box.x, msg_box.y))
                pygame.draw.rect(canvas, (255, 255, 255), msg_box, 2) 
                
                canvas.blit(text, text_rect)
                
                
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        
        return None