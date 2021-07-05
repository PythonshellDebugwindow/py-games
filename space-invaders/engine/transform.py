'''
    ***Transform class file***
    KHL Engine
    Created       May 07, 2020
    Last Modified Jun 23, 2020

    Remarks:
    -> Transform is a "basic behaviour",
       that "should" be added to all
       Game Objects
    -> This architecture is actually
       implemented in most other game
       engines
    -> Transforms govern a Game Object's
       location, rotation, and scale in
       the Game World (that is, the
       screen to which they're added)
    -> There should be no need to inherit
       from it, even though parenting is
       allowed. This was implemented to
       allow game objects to behave
       consistently, even though the
       parenting system may look redundant
    -> In that regard, the parent-child
       system is not yet fully implemented,
       but there should be no immediate
       need of it
'''
#Basic imports
#As Transform also relies on pygame's math,
#pygame and Vector2 are imported
import pygame
from pygame.math import Vector2
from engine.behaviour import Behaviour

class Transform(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "Transform"
        #self.parent should contain a reference
        #to the Game Object's parent Transform
        self.parent = None
        self.position = Vector2(0)
        self.rotation = 0
        self.scale = Vector2(1)
        
    def start(self):
        super().start()
        
    def update(self):
        super().update()
        '''
        #assumes parent is a Transform
        if self.parent != None:
            transf = self.game_object.get_behaviour("Transform")
            transf.position.x += self.parent.position.x
            transf.position.y += self.parent.position.y
            transf.rotation += self.parent.rotation
            transf.scale.x += self.parent.scale.x
            transf.scale.y += self.parent.scale.y
        '''
        
    def render(self):
        super().render()

    #Transform specific functionality:
    #translate() checks the incoming data type and
    #displaces the object accordingly
    def translate(self, translation):
        if isinstance(translation, Vector2):
            self.position.x += translation.x
            self.position.y += translation.y
            return #safety measure
        if isinstance(translation, (list, tuple)):
            self.position.x += translation[0]
            self.position.y += translation[1]
            return #safety measure
        if isinstance(translation, int):
            self.position.x += translation
            return #safety measure
        
        import sys
        print("TypeError in transform.translate: translation is",
              type(translation))
        pygame.quit()
        sys.exit()
        
    #rotate() basically just adds the rotation passed
    #as a parameter to the transform's current
    #rotation. As such, it does not check whether the
    #angle was passed in radians or degrees
    def rotate(self, _rotation):
        self.rotation += _rotation

    #rescale() works similarly to translate(), but it
    #also implements uniform scaling. This method was
    #named rescale() to avoid naming conflicts with
    #the scale attribute
    def rescale(self, _scale):
        if isinstance(_scale, (float, int)):
            self.scale.x *= _scale
            self.scale.y *= _scale
            return
        if isinstance(_scale, Vector2):
            self.scale.x *= _scale.x
            self.scale.y *= _scale.y
            return
        if isinstance(_scale, (list, tuple)):
            self.scale.x *= _scale[0]
            self.scale.y *= _scale[1]
            return
