'''
    Image Renderer class
    pygame "engine"
    Designed to test different effects
    THIS CODE REQUIRES HEAVY CLEANUP
'''
import pygame
from engine.behaviour import Behaviour

class ImageRenderer(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "ImageRenderer"
        self.img = pygame.image.load("assets/Images/player1.png")
        
    def start(self):
        super().start()
        
    def update(self):
        super().update()
        
    def render(self):
        surf = pygame.display.get_surface()
        tr = self.game_object.get_behaviour("Transform")
        #Creates rotated surface based on transform
        rotated_img = pygame.transform.rotate(self.img,
                                              tr.rotation).convert_alpha()
        #Corrected rotation
        center_x = int(tr.position.x - rotated_img.get_rect().width / 2)
        center_y = int(tr.position.y - rotated_img.get_rect().height / 2)
        #Actual draw to the screen, using properly rotated surfaces
        surf.blit(rotated_img, (center_x, center_y),
                  rotated_img.get_rect())

    def set_img(self, path):
        self.img = pygame.image.load(path)
