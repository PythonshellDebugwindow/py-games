'''
    Shield Renderer Class
    pygame "engine"
    Designed to test different effects
'''
import pygame
from engine.behaviour import Behaviour

class ShieldRenderer(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "ShieldRenderer"
        self.colour = pygame.Color(0, 255, 0, 125)
##        self.colour.cmy = (0.5, 1, 0.5)
        self.width = 105 #Width per row
        self.height = 15 #Height per row
        self.rows = [] #List of 0..5 rects, initialized in start()
        
    def start(self):
        pos = self.game_object.get_behaviour("Transform").position
        self.rows = [pygame.Rect(pos.x, pos.y + i * (self.height + 5),
                                 self.width, self.height) for i in range(5)]
        super().start()
    
    def update(self):
        super().update()
    
    def render(self):
        surf = pygame.display.get_surface()
        t = self.game_object.get_behaviour("Transform")
        
        for r in self.rows:
            sf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(sf, self.colour,
                             pygame.Rect(0, 0, self.width, self.height))
            surf.blit(sf, r, None, pygame.BLEND_RGBA_MULT)
    
    def remove_row(self):
        if len(self.rows) > 0:
            self.rows.pop()
