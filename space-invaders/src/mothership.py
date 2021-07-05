'''
    Mothership class
    pygame "engine"
    Designed to test different effects
'''
import pygame, random
from engine.game_object import GameObject
from engine.behaviour import Behaviour
from src.enemy_bullet_movement import EnemyBulletMovement
from src.bullet_renderer import BulletRenderer

class Mothership(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "Mothership"
        self.x = 0
        self.x_max = pygame.display.get_surface().get_width() - 50
        self.speed = 50
        self.image = pygame.image.load("assets/images/mothership.png")

        self.bullet_counter = 0
        self.shot_cooldown = 2000 #Milliseconds
        self.last_shot = 0
        self.has_shot = False
        self.move_cooldown = 500 #Milliseconds
        self.last_move = 0
        self.has_moved = False

    def start(self):
        super().start()

    def update(self):
        super().update()
        from engine.game_env import Game
        if self.has_moved:
            self.last_move += Game.instance.get_delta_time()
        if self.last_move > self.move_cooldown:
            self.last_move = 0
            self.has_moved = False
        if not self.has_moved:
            self.has_moved = True
            self.x += self.speed
            if self.x >= self.x_max:
                print("Mothership X offscreen")
                cs = Game.instance.current_screen
                cs.remove_game_object(self.game_object)
        self.shoot_player_with_cooldown()
    
    def render(self):
        super().render()
        surf = pygame.display.get_surface()
        surf.blit(self.image, (self.x, 25))

    def test_shot(self, bullet):
        pos = bullet.get_behaviour("Transform").position
        x, y = pos.x, pos.y
        x_w, y_h = pos.x, y - 70
        sy = self.game_object.get_behaviour("Transform").position.y
        sx, sx_w = self.x, self.x + 119
        sy_h = sy + 52
        if x >= sx and x <= sx_w and y <= sy_h:
            # or x_w == sx:
            print("Mothership HIT!")#;pygame.quit();raise 0
            from engine.game_env import Game
            cs = Game.instance.current_screen
            if "Player" in cs.game_objects:
                pd = cs.game_objects["Player"].get_behaviour("PlayerData")
                pd.score += 10
            cs.remove_game_object(bullet)
            cs.remove_game_object(self.game_object)

    def shoot_player_with_cooldown(self):
        from engine.game_env import Game
        
        if self.has_shot:
            self.last_shot += Game.instance.get_delta_time()
        if self.last_shot > self.shot_cooldown:
            self.last_shot = 0
            self.has_shot = False
        if not self.has_shot and random.randint(0, 2) == 0:
            self.has_shot = True
            self.shoot_player()
        
    def shoot_player(self):
        from engine.game_object import GameObject
        bullet = GameObject()
        bullet.name = "MothershipBullet" + str(self.bullet_counter)
        bullet.get_behaviour("Transform").position.x = self.x + 60
        bullet.get_behaviour("Transform").position.y = 0
        bullet.add_behaviour(EnemyBulletMovement())
        bullet.add_behaviour(BulletRenderer())
        bullet.get_behaviour("BulletRenderer").mothershipify()
        bullet.get_behaviour("BulletRenderer").do_rotate(180)
        GameObject.add_to_screen(bullet)
        self.bullet_counter += 1
