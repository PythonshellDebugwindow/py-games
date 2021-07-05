'''
    Button Behaviour Class
    KHL Engine
    Designed to demonstrate states
    and screen change
'''
#base imports
import pygame
from engine.behaviour import Behaviour

class ButtonBehaviour(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "ButtonBehaviour"
        self.is_hover = False
        self.is_pressed = False
        self.f_onclick = None

    def start(self):
        super().start()
        
    def update(self):
        transf = self.game_object.get_behaviour("Transform")
        collider = self.game_object.get_behaviour("BoxCollider")
        renderer = self.game_object.get_behaviour("RectRenderer")
        
        collider.box.center = transf.position
        renderer.rect.center = transf.position
        renderer.rect.width = collider.box.width
        renderer.rect.height = collider.box.height

        self.is_hover = collider.box.collidepoint(pygame.mouse.get_pos())
        mouse_buttons = pygame.mouse.get_pressed()
        self.is_pressed = self.is_hover and mouse_buttons[0]

        tr = self.game_object.get_behaviour("TextRenderer")
        
        if self.is_pressed:
            renderer.colour = (0, 255, 0)
            if self.f_onclick != None:
                self.f_onclick()
        elif self.is_hover:
            renderer.colour = (0, 0, 255)
            if tr != None:
                tr.colour = (175, 175, 175)
        else:
            renderer.colour = (255, 0, 0)
            if tr != None:
                tr.colour = (255, 255, 255)
            
    def render(self):
        super().render()

    def compute_text_offset(self):
        #Must have an attached TextRenderer
        tr = self.game_object.get_behaviour("TextRenderer")
        e = self.game_object.get_behaviour("BoxCollider").extent
        tr.offset = pygame.math.Vector2(-e.x / 2 + 15, -e.y / 2 + 10)
