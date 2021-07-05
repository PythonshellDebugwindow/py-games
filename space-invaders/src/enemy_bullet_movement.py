'''
    Enemy Bullet Movement class
    pygame "engine" example
    Designed to test different functionality
'''
import pygame, math
from engine.behaviour import Behaviour

class EnemyBulletMovement(Behaviour):
    def __init__(self):
        super().__init__()
        self.name = "EnemyBulletMovement"
        self.speed = 10
        
    def start(self):
        super().start()
        self.y_max = pygame.display.get_surface().get_height()
        
    def update(self):
        super().update()
        from engine.game_env import Game
        
        t = self.game_object.get_behaviour("Transform")
        rot = math.radians(t.rotation)
        target = [0,0]
        target[0] = 1 * self.speed * math.sin(rot)
        target[1] = 1 * self.speed * math.cos(rot)
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
        
        if t.position.y >= self.y_max:
            Game.instance.current_screen.remove_game_object(
                self.game_object)
##            print("(?) src.enemy_bullet_movement: Off-screen")

        if "Player" in Game.instance.current_screen.game_objects:
            el = Game.instance.current_screen.game_objects["Player"]
            el.get_behaviour("PlayerData").test_player_shot(self.game_object)
    
    def render(self):
        super().render()

    def check_shields(self):
        #Kind of a hack, as the positions are hard-coded
        spos = self.game_object.get_behaviour("Transform").position
        sx, sy = spos.x - 25, spos.y
        sx2 = spos.x + 25
        sx3 = spos.x
        n=25*2
        if sy > 450:
            if sx > 200-n and sx < 305:
                return 0
            elif sx > 450-n and sx < 555:
                return 1
            elif sx > 700-n and sx < 805:
                return 2
        return -1
