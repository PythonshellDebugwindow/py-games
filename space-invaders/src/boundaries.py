import pygame
from engine.behaviour import Behaviour

class Boundaries(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "Boundaries"
        width, height = pygame.display.get_surface().get_size()
        
        self.left = 0
        self.right = width - 1
        self.top = 0
        self.bottom = height - 1
        self.orig_left = 0
        self.orig_right = width - 1
        self.orig_top = 0
        self.orig_bottom = height - 1
        
        self.offset = pygame.math.Vector2(0, 0)
        self.do_wrap = False

    def start(self):
        super().start()

    def update(self):
        tr = self.game_object.get_behaviour("Transform")
        pos = tr.position
        
        if pos.x < self.left:
            tr.position.x = (self.right - 1) if self.do_wrap else self.left
        elif pos.x > self.right:
            tr.position.x = self.left if self.do_wrap else (self.right - 1)
        if pos.y < self.top:
            tr.position.y = (self.bottom - 1) if self.do_wrap else self.top
        elif pos.y > self.bottom:
            tr.position.y = self.top if self.do_wrap else (self.bottom - 1)

    def set_offset(self, offset):
        self.offset = offset
        self.left = self.orig_left + offset.x
        self.right = self.orig_right - offset.x
        self.top = self.orig_top + offset.y
        self.bottom = self.orig_bottom - offset.y
