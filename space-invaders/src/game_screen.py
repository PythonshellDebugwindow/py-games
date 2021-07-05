'''
    ***Game Screen class***
    Pygame "engine"
    Designed to test a couple effects
'''
import pygame
from engine.screen import Screen
from engine.game_object import GameObject
from engine.box_collider import BoxCollider
from engine.text_renderer import TextRenderer
#Behaviour imports
from src.rect_renderer import RectRenderer
from src.image_renderer import ImageRenderer
from src.linear_movement import LinearMovement
from src.shield_renderer import ShieldRenderer
from src.player_commands import PlayerCommands
from src.player_data import PlayerData
from src.boundaries import Boundaries
from src.screenshot_taker import ScreenshotTaker
from src.enemy_line import EnemyLine
from src.mothership import Mothership
#Convenience imports
from pygame.math import Vector2
from pygame import Rect

class GameScreen(Screen):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.mship_cooldown = 10_000 #Milliseconds
        self.last_mship = 0
        self.had_mship = True
        self.can_have_mship = True

    def start(self):
        print("(?) src.game_screen: start() called")
        self.image = pygame.image.load("assets/images/background.jpg")

        def player_death():
            from engine.game_env import Game
            from src.intro_screen import IntroScreen
            print("You died")
            Game.instance.set_screen(IntroScreen())

        lvl_go = GameObject()
        lvl_go.name = "LevelText"
        h = pygame.display.get_surface().get_height()
        lvl_go.get_behaviour("Transform").position = Vector2(10, h - 70)
        lvl_go.add_behaviour(TextRenderer())
        lvl_go.get_behaviour("TextRenderer").text = "Level " + str(self.level)
        lvl_go.get_behaviour("TextRenderer").set_size(90)
        self.add_game_object(lvl_go)
        
        play_go = GameObject()
        play_go.name = "Player"
        play_go.get_behaviour("Transform").position = Vector2(512, 700)
        play_go.add_behaviour(BoxCollider())
        play_go.get_behaviour("BoxCollider").is_debug = False
        play_go.get_behaviour("BoxCollider").extent = Vector2(150)
        play_go.add_behaviour(ImageRenderer())
        play_go.add_behaviour(PlayerCommands())
        play_go.add_behaviour(LinearMovement())
        play_go.add_behaviour(PlayerData())
        play_go.get_behaviour("PlayerData").death_func = player_death
        play_go.add_behaviour(Boundaries())
        play_go.get_behaviour("Boundaries").set_offset(Vector2(60, 0))
        play_go.add_behaviour(ScreenshotTaker())
        self.add_game_object(play_go)

        for i in range(3):
            sr_go = GameObject()
            sr_go.name = "Shield" + str(i)
            sr_go.get_behaviour("Transform").position.x = 200 + i * 250
            sr_go.get_behaviour("Transform").position.y = 500
            sr_go.add_behaviour(ShieldRenderer())
            self.add_game_object(sr_go)
        
        el_go = GameObject()
        el_go.name = "EnemyLine"
        el_go.add_behaviour(EnemyLine())
        self.add_game_object(el_go)

        print("(?) src.game_screen: start() done")
        
        super().start()
        
    def update(self):
        from engine.game_env import Game
        if self.had_mship:
            self.last_mship += Game.instance.get_delta_time()
        if self.last_mship > self.mship_cooldown:
            self.last_mship = 0
            self.had_mship = False
        if not self.can_have_mship and "Mothership" not in self.game_objects:
            self.can_have_mship = True
            self.last_mship = 0
        if not self.had_mship and self.can_have_mship:
            self.had_mship = True
            self.can_have_mship = False
            ms_go = GameObject()
            ms_go.name = "Mothership"
            ms_go.add_behaviour(Mothership())
            self.add_game_object(ms_go)
        
        if "Mothership" not in self.game_objects:
            if "EnemyLine" in self.game_objects:
                fl = open("assets/txt/SCORE.txt", "w")
                pd = self.game_objects["Player"].get_behaviour("PlayerData")
                fl.write(str(pd.score))
                fl.close()
                el = self.game_objects["EnemyLine"]
                if not el.get_behaviour("EnemyLine").populated:
                    print("All Enemies and Motherships are gone!")
                    print("Starting a new level")
                    gs = GameScreen()
                    gs.level = self.level + 1
                    Game.instance.set_screen(gs)
            else:
                raise Exception("No EnemyLine in GameScreen")
        
        super().update()
        
    def render(self):
        surf = pygame.display.get_surface()
        if self.bg_colour != None:
            surf.fill(self.bg_colour)
        if self.image != None:
            surf.blit(self.image, (0, 0))
        super().render()
        
    def add_game_object(self, game_object):
        super().add_game_object(game_object)
        
    def remove_game_object(self, game_object):
        super().remove_game_object(game_object)
