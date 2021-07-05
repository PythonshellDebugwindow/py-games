'''
    ***Screen base class file***
    KHL Engine
    Created       May 04, 2020
    Last Modified Jun 11, 2020

    Remarks:
    -> Base for all game screens, which will,
       in this case, correspond to game states
    -> Screens are basically containers of
       Game Objects, responsible to call update()
       and render() on them
    -> Due to an issue with iterating through
       dictionaries that are modified at runtime
       (as is the case when instantiating
       game objects), keys are cast into a list
       before iteration.
    -> Expanded the start() method
'''
import pygame
from engine.game_object import GameObject
#other imports go here

class Screen:
    def __init__(self):
        #Screens should support both bacground
        #colours and images
        self.bg_colour = None
        self.image = None
        self.game_objects = {}
        self.is_started = False
    
    def start(self):
        #This base class function must be called
        #at the end of each and every derived
        #screen start() implementation

        #This will start all Behaviours, regardless
        #of their being active or not
        for key in list(self.game_objects.keys()):
            if not self.game_objects[key].is_started:
                self.game_objects[key].start()
            
        #Start part
        if not self.is_started:
            self.is_started = True
            return

    #update() and render() run these same functions
    #on every active game object in the screen
    #-> The cast into a list is necessary to avoid
    #"dictionary size changed during iteration" errors
    def update(self):
        #may have custom functionality in children
        for key in list(self.game_objects.keys()):
            if self.game_objects[key].is_active:
                self.game_objects[key].update()

    def render(self):
        #may have custom functionality in children
        for key in list(self.game_objects.keys()):
            if self.game_objects[key].is_active:
                self.game_objects[key].render()

    #Screen specific functionality. Some levels of
    #error-checking were implemented, specifically
    #to prevent the duplicate insertion and override
    #of existing items
    #Starts Game Object behaviours when added
    def add_game_object(self, game_object):
        if (isinstance(game_object, GameObject)
            and game_object.name not in list(self.game_objects.keys())):
            self.game_objects[game_object.name] = game_object
            if not self.game_objects[game_object.name].is_started:
                self.game_objects[game_object.name].start()
    
    def remove_game_object(self, game_object):
        if game_object.name in list(self.game_objects.keys()):
            self.game_objects.pop(game_object.name)
