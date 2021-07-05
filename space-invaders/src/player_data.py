'''
    Player Data class
    Contains the player's health and score
    pygame "engine" example
    Designed to test different functionality
'''
import pygame
from engine.behaviour import Behaviour

class PlayerData(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "PlayerData"
        self.lives = 3
        self.score = 0
        try:
            self.score = int(open("assets/txt/SCORE.txt").read())
        except ValueError:
            print("Invalid int `" + open("assets/txt/SCORE.txt").read() + "'")
        self.font_path = "engine/engine_assets/Mozart-NBP.ttf"
        self.font = pygame.font.Font(self.font_path, 125)
        self.image = pygame.image.load("assets/images/heart.png")
        self.death_func = lambda: print("You died!")
    
    def update(self):
        super().update()
        
    def render(self):
        super().render()
        surf = pygame.display.get_surface()
        #Display lives
        for i in range(self.lives):
            surf.blit(self.image, (25 + i * 135, 25))
        #Display score
        r = self.font.render("Score: " + str(self.score).rjust(2, "0"), True,
                             (255, 255, 255))
        surf.blit(r, pygame.math.Vector2(500, 15))
    
    def decrease_lives(self):
        self.lives -= 1
        if self.lives == 0:
            from engine.game_env import Game
            el = Game.instance.current_screen.game_objects.get("EnemyLine")
            el.populated = False
            el.enemies = []
            fl = open("assets/txt/SCORE.txt", "w")
            fl.write(str(self.score))
            fl.close()
            self.death_func()
    
    def test_player_shot(self, bullet):
        pos = bullet.get_behaviour("Transform").position
        spos = self.game_object.get_behaviour("Transform").position
        sx, sy = spos.x - 55*2, spos.y
        sx_w = spos.x + 55*0
        x, y = pos.x-55, pos.y
        x_w, y_h = pos.x + 55*1, y + 70
        if x > sx and x < sx_w and y > sy:
            from engine.game_env import Game
            print("(?) Pdata: bullet+player collided",pos,spos)
            cs = Game.instance.current_screen
            self.decrease_lives()
            cs.remove_game_object(bullet)
