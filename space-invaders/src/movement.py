'''
    Movement Class file
    Pygame "engine"
    Designed to test different effects
'''
import pygame
import math
from engine.behaviour import Behaviour

class Movement(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "Movement"
        self.forward_speed = 10
        self.forward_info = 0
        self.rotation_speed = 2
        self.rotation_info = 0
        
    def start(self):
        super().start()
        
    def update(self):
        key_list = pygame.key.get_pressed()

        w = key_list[pygame.K_w]
        a = key_list[pygame.K_a]
        s = key_list[pygame.K_s]
        d = key_list[pygame.K_d]

        self.forward_info = 0
        self.rotation_info = 0

        #Note: pygame handles rotation counterclockwise
        if w:
            self.forward_info -= 1
        if a:
            self.rotation_info += 1
        if s:
            self.forward_info += 1
        if d:
            self.rotation_info -= 1

        self.forward_info *= self.forward_speed
        self.rotation_info *= self.rotation_speed

        #Needed for correct rotation
        rot = math.radians(self.rotation_info)
        
        t = self.game_object.get_behaviour("Transform")

        target = [0,0] #[x, y]
        #target[0] = self.forward_info*math.sin(rot)
        #target[1] = self.forward_info*math.cos(rot)
        t.rotate(self.rotation_info)

        '''
        # Redefining rotation:
        May sound counterintuitive to have sin for x
        and cos for y, but it happens because 0 degree
        is actually the ship's "forward", not the
        world's
        '''
        rot = math.radians(t.rotation)
        target[0] = self.forward_info*math.sin(rot)
        target[1] = self.forward_info*math.cos(rot)
        t.translate(target)

        '''
        if key_list[pygame.K_SPACE]:
            print(rot)
            print("sin:",math.sin(rot))
            print("cos:",math.cos(rot))
            print(target[0])
            print(target[1])
        '''
        
        def render(self):
            super().render()
