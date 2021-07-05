'''
    Intro Screen class
    KHL Engine
    Designed to demonstrate screen change
    and states
'''
#Base imports
import pygame
from engine.screen import Screen
from engine.game_object import GameObject
from engine.box_collider import BoxCollider
#Source-specific Behaviour imports
from src.rect_renderer import RectRenderer
from src.button_behaviour import ButtonBehaviour
from engine.text_renderer import TextRenderer
#Convenience imports
from pygame.math import Vector2

class IntroScreen(Screen):
    def __init__(self):
        super().__init__()

    def start(self):
        self.image = pygame.image.load("assets/images/background.jpg")
        
        def btnclick():
            from engine.game_env import Game
            from src.game_screen import GameScreen
            Game.instance.set_screen(GameScreen())
        
        btn_go = GameObject()
        btn_go.name = "Button"
        btn_go.get_behaviour("Transform").position = Vector2(512, 384)
        btn_go.add_behaviour(BoxCollider())
        btn_go.get_behaviour("BoxCollider").extent = Vector2(200, 100)
        btn_go.add_behaviour(TextRenderer())
        btn_go.get_behaviour("TextRenderer").text = "Start"
        btn_go.get_behaviour("TextRenderer").set_size(90)
        btn_go.add_behaviour(ButtonBehaviour())
        btn_go.get_behaviour("ButtonBehaviour").compute_text_offset()
        btn_go.get_behaviour("ButtonBehaviour").f_onclick = btnclick
        btn_go.add_behaviour(RectRenderer())
        self.add_game_object(btn_go)
        
        text_go = GameObject()
        text_go.name = "GameText"
        text_go.get_behaviour("Transform").position = Vector2(280, 200)
        text_go.add_behaviour(TextRenderer())
        text_go.get_behaviour("TextRenderer").text = "Space Reinvaders"
        text_go.get_behaviour("TextRenderer").set_size(100)
        self.add_game_object(text_go)
        
        i1_go = GameObject()
        i1_go.name = "Instr1"
        i1_go.get_behaviour("Transform").position = Vector2(280, 500)
        i1_go.add_behaviour(TextRenderer())
        i1_go.get_behaviour("TextRenderer").text = "Press space to shoot"
        i1_go.get_behaviour("TextRenderer").set_size(50)
        self.add_game_object(i1_go)
        i2_go = GameObject()
        i2_go.name = "Instr2"
        i2_go.get_behaviour("Transform").position = Vector2(280, 550)
        i2_go.add_behaviour(TextRenderer())
        i2_go.get_behaviour("TextRenderer").text = "Press A and D to move"
        i2_go.get_behaviour("TextRenderer").set_size(50)
        self.add_game_object(i2_go)
        
        super().start()
        
    def update(self):
        super().update()
        
    def render(self):
        surf = pygame.display.get_surface()
        if self.bg_colour != None:
            surf.fill(self.bg_colour)
        if self.image != None:
            surf.blit(self.image, (0,0))
        super().render()
        
    def add_game_object(self, go):
        super().add_game_object(go)
        
    def remove_game_object(self, go):
        super().remove_game_object(go)
