'''
    Temporary Renderer Class file
    pygame "engine"
    Designed to test different effects   
'''
import pygame
from engine.behaviour import Behaviour
#convenience imports
from pygame.math import Vector2

class RectRenderer(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "RectRenderer"
        self.colour = (255, 0, 0)
        self.extent = Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
    def start(self):
        self.rect.width = self.extent.x
        self.rect.height = self.extent.y
        super().start()
    def update(self):
        super().update()
        #Figured this would make more sense here
        t = self.game_object.get_behaviour("Transform")
        self.rect.center = Vector2(t.position)
    def render(self):
        surf = pygame.display.get_surface()
        if self.rect.width > 0 < self.rect.height:
            pygame.draw.rect(surf, self.colour, self.rect, 5)
