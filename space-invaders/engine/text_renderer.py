import pygame, os
from engine.behaviour import Behaviour

class TextRenderer(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "TextRenderer"
        self.text = "Hello World"
        self.size = 12
        self.offset = pygame.math.Vector2(0,0) #Mainly for button_behaviour.py
        self.colour = (255, 255, 255)
        
        self.font_path = "engine/engine_assets/Mozart-NBP.ttf"
        if not os.path.isfile(self.font_path):
            self.font_path = "assets/fonts/Mozart-NBP.ttf"
        self.do_antialias = True

        self.generate_font()
        self.display = pygame.display.get_surface()

        self.transform = None

    def start(self):
        super().start()
        self.transform = self.game_object.get_behaviour("Transform")

    def generate_font(self):
        self.font = pygame.font.Font(self.font_path, self.size)

    #Need to update the font through this method since we don't want
    #to create a new Font object every frame
    def set_size(self, size):
        self.size = size
        self.generate_font()
    
    def set_font(self, font_path):
        self.font_path = font_path
        self.generate_font()
    
    def update(self):
        super().update()
        
    def render(self):
        super().render()
        text_surface = self.font.render(self.text, self.do_antialias,
                                        self.colour)
        self.display.blit(text_surface, self.transform.position + self.offset)
