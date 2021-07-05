'''
    ***Behaviour base class file***
    KHL Engine
    Created       May 04, 2020
    Last Modified Jun 11, 2020

    Remarks:
    -> A Behaviour is simply an empty
       base class, written to enforce
       consistency between different
       behaviours and to act as a
       type-check safety feature in the
       game objects
    -> Specific functionality should be
       implemented in derived classes
    -> This class has a reference to
       whichever game object is its
       parent. This is useful to manage
       cross-behaviour interactions
    -> As expected, update() and render()
       are empty functions, which expect
       implementation in derived
       behaviours
    -> The only function that actually has
       functionality is start(). This sets
       the is_started variable to true,
       other classes should check whether
       the behaviour is started before
       calling this method in children
    -> This class vaguely mirrors Unity's
       "MonoBehaviour" architecture, and
       was actually designed with that
       functionality in mind
'''

class Behaviour:
    def __init__(self):
        self.name = ""
        self.game_object = None
        self.is_started = False
        self.is_active = True
    def start(self):
        self.is_started = True
    def update(self):
        pass
    def render(self):
        pass
