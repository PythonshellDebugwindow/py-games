'''
    Player Commands class
    pygame "engine"
    Designed to test different effects
'''
import pygame
from engine.behaviour import Behaviour
from src.bullet_movement import BulletMovement
from src.bullet_renderer import BulletRenderer

class PlayerCommands(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "PlayerCommands"
        self.cooldown = 500 #Milliseconds
        self.has_shot = False
        self.last_shot = 0
        self.bullet_counter = 0
        
    def start(self):
        super().start()
        
    def update(self):
        super().update()

        #TEST
        if pygame.key.get_pressed()[pygame.K_BACKSLASH]:
            print("Lost a life")
            h = self.game_object.get_behaviour("PlayerData")
            if h != None:
                h.decrease_lives()
            else:
                print("Null PlayerData")
        #END TEST
        
        shoot_key = pygame.key.get_pressed()[pygame.K_SPACE]

        #Simplified, but necessary for clock
        from engine.game_env import Game

        if self.has_shot:
            self.last_shot += Game.instance.get_delta_time()
        if self.last_shot > self.cooldown:
            self.last_shot = 0
            self.has_shot = False
        if shoot_key and not self.has_shot:
            self.shoot()

    def render(self):
        super().render()

    def shoot(self):
        self.has_shot = True

        from engine.game_object import GameObject
        bullet = GameObject()
        bullet.name = "Bullet" + str(self.bullet_counter)
        tr = self.game_object.get_behaviour("Transform")
        bullet.get_behaviour("Transform").position.x = tr.position.x - 12
        bullet.get_behaviour("Transform").position.y = tr.position.y - 54
        bullet.get_behaviour("Transform").rotation = tr.rotation
        bullet.add_behaviour(BulletMovement())
        bullet.add_behaviour(BulletRenderer())
        GameObject.add_to_screen(bullet)
        self.bullet_counter += 1
