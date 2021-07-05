'''
    Enemy Line class
    has all the functionality of a line of enemies
    pygame "engine" example
    Designed to test different functionality
'''
import pygame, random
from pygame.math import Vector2
from engine.behaviour import Behaviour
from src.bullet_renderer import BulletRenderer
from src.enemy_bullet_movement import EnemyBulletMovement

class EnemyLine(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "EnemyLine"
        self.enemy_img = pygame.image.load("assets/images/enemy-xsml.png")
        self.speed = 25
        self.rows = 5 #1 for mothership testing, 5 otherwise
        self.cols = 3 #1 for mothership testing, 3 otherwise
        self.enemies = [] #Initialized in start()
        self.populated = True
        self.bullet_counter = 0
        
        self.is_going_left = False
        self.x_max = pygame.display.get_surface().get_width() - 115
        self.move_cooldown = 500 #Milliseconds
        self.last_move = 0
        self.has_moved = False
        self.shot_cooldown = 125 #Milliseconds
        self.last_shot = 0
        self.has_shot = False
        
    def start(self):
        pos = self.game_object.get_behaviour("Transform").position
        for i in range(self.rows):
            for j in range(self.cols):
                self.enemies.append(Vector2(pos.x + i * 125 + 10,
                                            pos.y + j * 90 + 90))
        super().start()
        
    def update(self):
        super().update()
        if pygame.key.get_pressed()[pygame.K_p]:self.shoot_player(100) #TEST
        
        if self.populated:
            if len(self.enemies) < 1:
                self.populated = False
            else:
                self.move_with_cooldown()
                self.shoot_player_with_cooldown()
    
    def render(self):
        super().render()
        if self.populated:
            surf = pygame.display.get_surface()
            for enemy in self.enemies:
                surf.blit(self.enemy_img, (enemy.x, enemy.y))

    def move_with_cooldown(self):
        from engine.game_env import Game
        if self.has_moved:
            self.last_move += Game.instance.get_delta_time()
        if self.last_move > self.move_cooldown:
            self.last_move = 0
            self.has_moved = False
        if not self.has_moved:
            self.has_moved = True
            self.move()
    
    def move(self):
        if self.is_going_left:
            if self.enemies[0].x <= 20:
                self.is_going_left = False
                for enemy in self.enemies:
                    enemy += Vector2(0, 70)
            else:
                for enemy in self.enemies:
                    enemy -= Vector2(self.speed, 0)
        else:
            if self.enemies[-1].x >= self.x_max:
                self.is_going_left = True
                for enemy in self.enemies:
                    enemy += Vector2(0, 70)
            else:
                for enemy in self.enemies:
                    enemy += Vector2(self.speed, 0)
    
    #Removes the enemy touching the bullet if there is one (e.g. it was hit)
    def test_enemy_shot(self, bullet):
        if self.populated:
            pos = bullet.get_behaviour("Transform").position
            x, y = pos.x - 115, pos.y
            x_w, y_h = pos.x, y - 70
            for i, enemy in enumerate(reversed(self.enemies)):
                if (x <= enemy.x <= x_w and enemy.y >= y_h) or x_w == enemy.x:
                    from engine.game_env import Game
                    self.enemies.pop(len(self.enemies) - i - 1)
                    cs = Game.instance.current_screen
                    if "Player" not in cs.game_objects:
                        return
                    pd = cs.game_objects["Player"].get_behaviour("PlayerData")
                    pd.score += 1
                    cs.remove_game_object(bullet)
                    return

    def shoot_player_with_cooldown(self):
        from engine.game_env import Game
        
        if self.has_shot:
            self.last_shot += Game.instance.get_delta_time()
        if self.last_shot > self.shot_cooldown:
            self.last_shot = 0
            self.has_shot = False
        if not self.has_shot and random.randint(0, 16) == 0:
            self.has_shot = True
            x = random.choice(list({e.x for e in self.enemies}))
            self.shoot_player(x)
        
    def shoot_player(self, x):
        from engine.game_object import GameObject
        bullet = GameObject()
        bullet.name = "EnemyBullet" + str(self.bullet_counter)
        bullet.get_behaviour("Transform").position.x = x
        bullet.get_behaviour("Transform").position.y = 200
        bullet.add_behaviour(EnemyBulletMovement())
        bullet.add_behaviour(BulletRenderer())
        bullet.get_behaviour("BulletRenderer").do_rotate(180)
        GameObject.add_to_screen(bullet)
        self.bullet_counter += 1
