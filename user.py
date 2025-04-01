from enum import Enum
import numpy as np
import pygame
import os



TILE_SIZE = 64 # 64x64 pixels of ghost img size

COLORS = {
    0: (200, 200, 200),  # Empty/path - light gray
    1: (100, 100, 100)  # Wall - dark gray
}

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


WIDTH = TILE_SIZE * len(maze[0])
HEIGHT = TILE_SIZE * len(maze)

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

player = Actor("ghost", anchor=(0, 0), pos=(1 * TILE_SIZE, 1 * TILE_SIZE))


message = ""
show_message = False
message_timer = 0
MESSAGE_DURATION = 3.0 



def draw():

    screen.clear()
    surface = screen.surface
    
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            cell_type = maze[row][column]
            
            if cell_type == 2:

                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, COLORS[0], rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 1) # border
                screen.blit("home", (x, y))
            else :  

                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)         
                pygame.draw.rect(surface, COLORS[cell_type], rect)              
                pygame.draw.rect(surface, (50, 50, 50), rect, 1)  
    
    player.draw()

    if show_message:
       

        message_width = len(message) * 15  
        message_width = max(message_width, 160) 
        message_width = min(message_width, WIDTH * 0.6)
        message_box = pygame.Rect(
            (WIDTH - message_width) // 2, 
            HEIGHT * 0.4,                  
            message_width,                 
            HEIGHT * 0.15                  
        )

        message_box.height += 30 

        s = pygame.Surface((message_box.width, message_box.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  
        surface.blit(s, (message_box.x, message_box.y))
        pygame.draw.rect(surface, (255, 255, 255), message_box, 2)
        
        screen.draw.text(message, 
                center=(message_box.centerx, message_box.centery - 10), 
                color="yellow", 
                fontsize=30, 
                shadow=(1, 1),
                owidth=1.5,
                ocolor="black")

        screen.draw.text("Press 'R' to restart", 
                         center=(message_box.centerx, message_box.centery + 25), 
                         color="white", 
                         fontsize=20)

def update(dt):

    global show_message, message_timer
    
    if show_message : 
        message_timer -= dt
        if message_timer <= 0:
            show_message = False


def on_key_down(key):
    global goals_found, show_message, message_timer, message 
    
  
    if key == keys.R : 
        restart_game()
        return
        
    # Player movement
    x, y = player.pos
    row = int(y // TILE_SIZE)
    col = int(x // TILE_SIZE)
    
    new_row, new_col = row, col
    
    if key == keys.UP:
        new_row = row - 1
    elif key == keys.DOWN:
        new_row = row + 1
    elif key == keys.LEFT:
        new_col = col - 1
    elif key == keys.RIGHT:
        new_col = col + 1
    
    if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != 1:
        player.pos = (new_col * TILE_SIZE, new_row * TILE_SIZE)
        

        if maze[new_row][new_col] == 2:

            show_message = True
            message_timer = MESSAGE_DURATION
            
            maze[new_row][new_col] = 0
            
            message = "GOAL REACHED!"

            

def restart_game():

    global  show_message, message  
    
    player.pos = (1 * TILE_SIZE, 1 * TILE_SIZE)
    
    for row in range(len(maze)):
        for col in range(len(maze[row])):

            if (row == 18 and col == 18) : 
                maze[row][col] = 2
    
    show_message = False
    message = ""







#  def render(self):

#         if self.render_mode == "human":
#             if self.window is None:
#                 pygame.init()
#                 pygame.display.init()
#                 self.window = pygame.display.set_mode((self.window_size, self.window_size))
#             if self.clock is None:
#                 self.clock = pygame.time.Clock()
        
        
#             self.agent_img = pygame.image.load("/home/souha/pac-man/images/ghost.png").convert_alpha()
#             self.target_img= pygame.image.load("/home/souha/pac-man/images/home.png").convert_alpha()
            
#             canvas = pygame.Surface((self.window_size, self.window_size))
#             canvas.fill((0, 0, 0))
            
#             # Draw maze
#             for i in range(len(self.maze)):
#                 for j in range(len(self.maze[i])):
#                     if self.maze[i][j] == 1:  # Wall
#                         pygame.draw.rect(
#                             canvas,
#                             (0, 0, 255),  # Blue
#                             pygame.Rect(
#                                 j * self.size, i * self.size, 
#                                 self.size, self.size
#                             ),
#                         )
                       
#                     if self.maze[i][j] == 2:  # Goal
#                         pygame.draw.rect(
#                             canvas,
#                             (0, 255, 0),  # Green
#                             pygame.Rect(
#                                 j * self.size, i * self.size, 
#                                 self.size, self.size
#                             ),
#                         )
                
#             # Draw agent
#             # pygame.draw.circle(
#             #     canvas,
#             #     (255, 0, 0),  # Red
#             #     (self._agent_location[0] * self.size + self.size // 2, 
#             #      self._agent_location[1] * self.size + self.size // 2),
#             #     self.size // 3,
#             # )

#             canvas.blit(
#                 self.agent_img,
#                 (self._agent_location[0] * self.size ,
#                  self._agent_location[1] * self.size )
#             )
            
#             self.window.blit(canvas, canvas.get_rect())
#             pygame.event.pump()
#             pygame.display.update()
#             self.clock.tick(self.metadata["render_fps"])
            
#         return None  