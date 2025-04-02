#!/usr/bin/env python3
import os
import sys
import pygame
# import tkinter as tk
# from tkinter import messagebox
import subprocess
import importlib
import gymnasium
import gymnasium_env


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100
BUTTON_MARGIN = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
DARK_BLUE = (70, 120, 220)

title_font = pygame.font.SysFont("Arial", 48, bold=True)
button_font = pygame.font.SysFont("Arial", 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")


# def check_requirements():
#     required_modules = ['pygame', 'gymnasium', 'stable_baselines3', 'numpy']
#     missing_modules = []
    
#     for module in required_modules:
#         try:
#             importlib.import_module(module)
#         except ImportError:
#             missing_modules.append(module)
    
#     required_files = [
#         'user.py',  
#         'ai_agent.py',  
#         'trained_maze_model.zip'  
#     ]

#     missing_files = []
    
#     for file in required_files:
#         if not os.path.exists(file):
#             missing_files.append(file)
    
#     if missing_modules or missing_files:
#         error_msg = "Missing requirements:\n"
#         if missing_modules:
#             error_msg += "Modules: " + ", ".join(missing_modules) + "\n"
#         if missing_files:
#             error_msg += "Files: " + ", ".join(missing_files)
        
#         root = tk.Tk()
#         root.withdraw() 
#         messagebox.showerror("Missing Requirements", error_msg)
#         root.destroy()
#         return False
        
#     return True


class Button:

    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):

        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        text_surface = button_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos) 

user_button = Button(
    (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
    SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN // 2,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    "Play Yourself",
    BLUE,
    DARK_BLUE
)

ai_button = Button(
    (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
    SCREEN_HEIGHT // 2 + BUTTON_MARGIN // 2,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    "Watch AI Play",
    BLUE,
    DARK_BLUE
)


def launch_game_mode(mode):
    if mode == "user":
        subprocess.run(["pgzrun", "user.py"])
    elif mode == "ai":
        subprocess.run(["python3", "ai_agent.py"])

# Main game loop
def main_menu():
    running = True
    
    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if user_button.is_clicked(mouse_pos):
                    launch_game_mode("user")
                
                if ai_button.is_clicked(mouse_pos):
                    launch_game_mode("ai")
        
        
        mouse_pos = pygame.mouse.get_pos()
        user_button.check_hover(mouse_pos)
        ai_button.check_hover(mouse_pos)
        
       
        screen.fill(GRAY)
        
        title_text = title_font.render("Maze Game", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        user_button.draw(screen)
        ai_button.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    
    # if check_requirements():
        main_menu()