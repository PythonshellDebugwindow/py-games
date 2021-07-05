'''
    Bullet Movement class
    pygame "engine"
'''
import math
from engine.behaviour import Behaviour

class BulletMovement(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "BulletMovement"
        self.speed = 10
        
    def start(self):
        #self.game_object.get_behaviour("Transform").position.y-=400 #Test
        super().start()
        
    def update(self):
        super().update()
        from engine.game_env import Game
        
        t = self.game_object.get_behaviour("Transform")
        rot = math.radians(t.rotation)
        target = [0,0]
        target[0] = -1 * self.speed * math.sin(rot)
        target[1] = -1 * self.speed * math.cos(rot)
        t.translate(target)

        cksh = self.check_shields()
        gos = Game.instance.current_screen.game_objects
        if cksh != -1 and ("Shield" + str(cksh)) in gos:
            sh = Game.instance.current_screen.game_objects["Shield"+str(cksh)]
            if len(sh.get_behaviour("ShieldRenderer").rows) > 0:
                sh.get_behaviour("ShieldRenderer").remove_row()
                Game.instance.current_screen.remove_game_object(
                    self.game_object)
                del gos
                return
        del gos

        if t.position.y < 0:
            Game.instance.current_screen.remove_game_object(self.game_object)
##            print("(?) src.bullet_movement: Off-screen")

        if "EnemyLine" in Game.instance.current_screen.game_objects:
            el = Game.instance.current_screen.game_objects["EnemyLine"]
            el.get_behaviour("EnemyLine").test_enemy_shot(self.game_object)
        else:
            print("Null EnemyLine GO")
        if "Mothership" in Game.instance.current_screen.game_objects:
            ms = Game.instance.current_screen.game_objects["Mothership"]
            ms.get_behaviour("Mothership").test_shot(self.game_object)
##        else:
##            print("Null Mothership GO")

    def render(self):
        super().render()
    
    def check_shields(self):
        #Kind of a hack, as the positions are hard-coded
        spos = self.game_object.get_behaviour("Transform").position
        sx, sy = spos.x - 25, spos.y
        sx2 = spos.x + 25
        sx3 = spos.x
        n=25*2
        if sy < 650:
            if sx > 200 - n and sx < 305:
                return 0
            elif sx > 450 - n and sx < 555:
                return 1
            elif sx > 700 - n and sx < 805:
                return 2
        return -1
