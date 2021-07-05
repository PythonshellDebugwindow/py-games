'''
    ***Box Collider class file***
    KHL Engine
    Created       Jun 01, 2020
    Last Modified Jul 12, 2020

    Remarks:
    -> This class implements an AABB
       collision model for the engine
    -> It inherits from Behaviour, but
       also relies on pygame's Rect()
       functionality
    -> Work is currently underway to
       implement overlap prevention
    -> In the future, part of this class
       may be reworked into a generic
       collider behaviour, where a
       Box Collider would be a specialization
       through inheritance
    -> It currently centers the collider on
       the parent Game Object's Transform
       behaviour, but it also supports offseting
       via the self.offset attribute
    -> A note on the is_debug flag:
       This flag enables or disables the
       collider's rendering, usually for debug
       purposes. Note that, to prevent distortions
       and rescaling if the parent game object is
       rotated, these colliders do not rotate with
       the parent (which is the basis of AABB
       collision to begin with)
'''
#Basic imports
#Colliders rely heavily on pygame Rects and
#pygame's math module
import pygame
from pygame import Rect
from pygame.math import Vector2
from engine.behaviour import Behaviour

class BoxCollider(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "BoxCollider"
        self.is_trigger = False
        self.center = Vector2(0,0)
        self.offset = Vector2(0,0)
        self.extent = Vector2(0,0)
        self.box = Rect(0,0,0,0)
        self.is_debug = False
    def start(self):
        super().start()
        t = self.game_object.get_behaviour("Transform")
        self.center = Vector2(t.position)
        self.center.x += self.offset.x
        self.center.y += self.offset.y
        self.box.center = self.center
        self.box.width = int(self.extent.x)
        self.box.height = int(self.extent.y)
    def update(self):
        super().update()
        #Code repeated to account for runtime collider changes
        t = self.game_object.get_behaviour("Transform")
        self.center = Vector2(t.position)
        self.center.x += self.offset.x
        self.center.y += self.offset.y
        self.box.center = self.center
        self.box.width = int(self.extent.x)
        self.box.height = int(self.extent.y)
    def render(self):
        super().render()
        if self.is_debug:
            surf = pygame.display.get_surface()
            pygame.draw.rect(surf, (0, 255, 0), self.box, 1)

    #collider-specific methods
    #overlaps() is designed for AABB only
    def overlaps(self, other):
        if isinstance(other, BoxCollider):
            return self.box.colliderect(other.box)
    #WIP
    #prevent_overlap forces the current box away from the other
    def prevent_overlap(self, other):
        if (isinstance(other, BoxCollider) and
            self.box.colliderect(other.box)):
            o = other.game_object.get_behaviour("Transform")
            r = self.box.clip(other.box)
            t = self.game_object.get_behaviour("Transform")
            
            ###################################################
            #Solution: Check for the smallest axis overlap and#
            #displace the invoking object's collider box back #
            #along it.                                        #
            #Obs.: This prevents overlap, but still causes a  #
            #small penetration depth due to the ship's speed. #
            #More elaborate calculations will probably be     #
            #needed, but the current approach should suffice  #
            #for the intended objective.                      #
            ###################################################

            if r.width < r.height:
                #if the other is to the right, push back to the left
                if o.position.x >= t.position.x:
                    t.position.x -= (r.width +1)
                else:
                    t.position.x += (r.width +1)
            else:
                #if the other is below, push it up
                if o.position.x >= t.position.y:
                    t.position.y -= (r.height +1)
                else:
                    t.position.y += (r.height +1)
