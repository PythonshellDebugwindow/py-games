'''
    Bullet Renderer class
    pygame "engine" example
    Designed to test different functionality
'''
import pygame
from engine.behaviour import Behaviour

class BulletRenderer(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "BulletRenderer"
        self.colour = (255, 255, 0)
        self.radius = 5
        self.image = pygame.image.load("assets/images/bullet-fire-sml1.png")
        
    def start(self):
        super().start()
        
    def update(self):
        super().update()
        
    def render(self):
        super().render()
        surf = pygame.display.get_surface()
        t = self.game_object.get_behaviour("Transform")
        pos = (int(t.position.x), int(t.position.y))
        
        #Render proper
        surf.blit(self.image, pos)

    def do_rotate(self, rotation):
        self.image = pygame.transform.rotate(self.image, rotation)

    def mothershipify(self):
        self.image = pygame.image.load("assets/images/bullet-ms-sml1.png")
        self.image = pygame.transform.scale(self.image, (24, 44))
