'''
    ***Game Object class file***
    KHL Engine
    Created       May 04, 2020
    Last Modified Jun 11, 2020

    Remarks:
    -> This class is based on Game Objects/Actors
       from other engines. This approach makes it easier
       for students to transition to other platforms and
       development software should they desire to do so
    -> A "Game Object" should not, at first, be inherited
       from; that is, it should not be thought of as a
       base class. Game Objects are usually containers
       for Behaviours and other Game Objects, without
       further specialization on a class-level
    -> The class follows a "behaviour-then-children"
       architecture. The reason is pretty much
       straightforward: any behaviour that alters
       the parent should be reflected in the children
    -> Game Objects now have an is_started variable, to
       account for the start() method calls
    -> Similar to the "Screen" issue with dictionaries,
       casting to a list is necessary before iteration
    -> Parent-child functionality not fully implemented,
       but students are not yet expected to handle this
       kind of semantics
    -> Possible future add-on: Functionality of the type
       "GameObject.Instantiate(model)"
'''
#Basic imports
#In general, Game Objects shouldn't know more than this
from engine.behaviour import Behaviour
from engine.transform import Transform

class GameObject:
    def __init__(self):
        #Each game object should have a unique name
        self.name = ""
        self.parent = None
        self.is_started = False
        self.is_active = True
        
        #Following other engines' architectures, Game
        #Objects are basically containers for behaviours
        #and other Game Objects.
        self.behaviours = {}
        self.children = {}
        
        #all game objects should have a transform
        #used the GameObject's own add_behaviour
        #functionality, to ensure consistency
        self.add_behaviour(Transform())

    def start(self):
        if not self.is_started:
            #calls start() on all "unstarted" behaviours and
            #children. As per the current architecture, it may
            #seem redundant, but it is more of a security check.
            for behaviour_name in list(self.behaviours.keys()):
                if not self.behaviours[behaviour_name].is_started:
                    self.behaviours[behaviour_name].start()
            for child_name in list(self.children.keys()):
                if not self.children[child_name].is_started:
                    self.children[child_name].start()
            self.is_started = True
        
    def update(self):
        #Opted for a behaviour-then-child architecture
        for behaviour_name in list(self.behaviours.keys()):
            if self.behaviours[behaviour_name].is_active:
                self.behaviours[behaviour_name].update()
        for child_name in list(self.children.keys()):
            if self.children[child_name].is_active:
                self.children[child_name].update()

    def render(self):
        #see update()
        for behaviour_name in list(self.behaviours.keys()):
            if self.behaviours[behaviour_name].is_active:
                self.behaviours[behaviour_name].render()
        for child_name in list(self.children.keys()):
            if self.children[child_name].is_active:
                self.children[child_name].render()

    #Behaviour management functionality
    #Implements type checking and name verification
    #to prevent addition of non-behaviours and duplicates
    def add_behaviour(self, behaviour):
        if (isinstance(behaviour, Behaviour) and
            behaviour.name not in list(self.behaviours.keys())
            and behaviour.game_object == None):
            behaviour.game_object = self
            self.behaviours[behaviour.name] = behaviour
            if not self.behaviours[behaviour.name].is_started:
                self.behaviours[behaviour.name].start()

    def remove_behaviour(self, behaviour):
        if behaviour.name in list(self.behaviours.keys()):
            self.behaviours[behaviour.name].game_object = None
            self.behaviours.pop(behaviour.name)

    #Behaviour getter. First checks whether the behaviour
    #exists in the current Game Object. Returns None as a
    #safety measure.
    def get_behaviour(self, behaviour_name):
        if behaviour_name in list(self.behaviours.keys()):
            return self.behaviours[behaviour_name]
        return None

    #Child management functionality
    #Implements the same type and duplicate-checking of
    #the behaviour dictionary
    def add_child(self, child):
        if (isinstance(child, GameObject) and
            child.name not in self.children.keys()
            and child.parent != null):
            child.parent = self
            self.children[child.name] = child
            if not self.children[child.name].is_started:
                self.children[child.name].start()

    #"This is to prevent multiple "import Game" statements
    @staticmethod
    def add_to_screen(game_obj):
        from engine.game_env import Game
        Game.instance.current_screen.add_game_object(game_obj)
