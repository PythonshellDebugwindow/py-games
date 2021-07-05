'''
    Linear Movement class
    Moves horizontally
    Pygame "engine"
    Designed to test different effects
'''
import pygame
import math
from engine.behaviour import Behaviour

class LinearMovement(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "LinearMovement"
        self.movement_info = 0
        self.speed = 25
        self.cooldown = 125 #Milliseconds
        self.last_move = 0
        self.has_moved = False
        
    def start(self):
        super().start()
        
    def update(self):
        super().update()
        key_list = pygame.key.get_pressed()
        
        a = key_list[pygame.K_a]
        d = key_list[pygame.K_d]

        self.movement_info = 0

        if a:
            self.movement_info -= 1
        if d:
            self.movement_info += 1

        #Simplified, but necessary for clock
        from engine.game_env import Game
        
        if self.has_moved:
            self.last_move += Game.instance.get_delta_time()
        if self.last_move > self.cooldown:
            self.last_move = 0
            self.has_moved = False
        if (a or d) and not self.has_moved:
            self.has_moved = True
            self.movement_info *= self.speed

            t = self.game_object.get_behaviour("Transform")
            t.translate(self.movement_info)
        
        def render(self):
            super().render()
