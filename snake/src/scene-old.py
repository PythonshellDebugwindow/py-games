from pygame import Color, Rect, Surface, K_SPACE
from pygame.draw import rect as draw_rect, circle as draw_circle
from pygame.math import Vector2
from pygame.key import get_pressed as get_pressed_keys
from pygame.font import SysFont

from src.collectible import Collectible

class Scene:
    def __init__(self):
        self.started = False
        
        self.fill_colour_min = Color(200, 167, 238)
        self.fill_colour_max = Color(138, 167, 200)
        
        self.circ_colour_min = Color(100, 20, 55)
        self.circ_colour_max = Color(0, 66, 127)
        
        self.circ_pos_min = Vector2(50, 50)
        self.circ_pos_max = Vector2(350, 350)
        
        self.lerp_n = 0
        self.lerp_speed = 0.05

        self.bg_colour = (240, 160, 212)
        self.area_info = (0, 0, 450, 450)
        self.cell_amt = 18
        self.back_colour = Color(231, 242, 198)
        self.cell_colour = Color(200, 200, 227)

        self.cell_size = (self.area_info[2] // self.cell_amt,
                          self.area_info[3] // self.cell_amt)
        self.play_rect = Rect(self.area_info)
        self.play_surf = Surface(self.area_info[2:])
        self.play_surf.fill(self.back_colour)

        self.circ_radius = 25
        
        self.fruit = Collectible(self.cell_size, self.cell_amt)
        
        self.draw_checkerboard()

        self.font = SysFont("Arial", 30)
        self.text = self.font.render("Text on screen.", False, self.bg_colour)
    
    def draw_checkerboard(self):
        for i in range(self.cell_amt):
            for j in range(self.cell_amt):
                if (i % 2 == 0) ^ (j % 2 == 0):
                    cr = Rect((i * self.cell_size[0], j * self.cell_size[1]),
                              self.cell_size)
                    draw_rect(self.play_surf, self.cell_colour, cr)
    
    def start(self):
        self.fruit.start()
        self.started = True
        return self.started
    
    def update(self, delta):
        space = get_pressed_keys()[K_SPACE]
        close = self.circs_are_close(threshold=15)
        if space or close:
            self.fruit.reposition()
        self.fruit.update(delta)
        
        self.progress_lerp()
    
    def progress_lerp(self):
        lssign = (abs(self.lerp_speed) / self.lerp_speed
                  if self.lerp_speed != 0
                  else 1)
        lspeed = (1 - abs(0.5 - self.lerp_n)) / 20 * lssign / 1.5
        self.lerp_n += lspeed #self.lerp_speed
        
        if self.lerp_n > 1 or self.lerp_n < 0:
            self.lerp_speed = -self.lerp_speed
            self.lerp_n -= lspeed #self.lerp_speed
    
    def get_lerped_circ_pos(self):
        return self.circ_pos_min.lerp(self.circ_pos_max, self.lerp_n)
    
    def circs_are_close(self, *, threshold=80):
        circ_pos_tuple = tuple(self.get_lerped_circ_pos())
        neg_circ_pos = (circ_pos_tuple[0],
                        self.circ_pos_max[1] - circ_pos_tuple[1])
        
        diff = abs(circ_pos_tuple[1] - neg_circ_pos[1])
        circs_are_close = diff <= threshold
        return circs_are_close
    
    def render(self, target):
        target.fill(self.bg_colour)
        
        lerped_fill_colour = self.fill_colour_min.lerp(self.fill_colour_max,
                                                       self.lerp_n)
        lerped_circ_colour = self.circ_colour_min.lerp(self.circ_colour_max,
                                                       self.lerp_n)
        lerped_rect_colour = self.circ_colour_min.lerp(self.circ_colour_max,
                                                       1 - self.lerp_n)
        if self.circs_are_close():
            target.fill((255, 0, 0))
        else:
            target.fill(lerped_fill_colour)
        
        actual_circ_colour = ((255, 0, 0)
                              if self.circs_are_close()
                              else lerped_circ_colour)
        actual_rect_colour = ((255, 0, 0)
                              if self.circs_are_close()
                              else lerped_rect_colour)
        
        target.blit(self.play_surf, self.play_rect)
        self.fruit.render(target)
        
        circ_pos_tuple = tuple(self.get_lerped_circ_pos())
        neg_circ_pos = (circ_pos_tuple[0],
                        self.circ_pos_max[1] - circ_pos_tuple[1])
        
        draw_circle(target, actual_circ_colour,
                    circ_pos_tuple, self.circ_radius)
        draw_rect(target, actual_rect_colour,
                  Rect((circ_pos_tuple[0] - self.circ_radius // 2,
                        circ_pos_tuple[1] - self.circ_radius // 2),
                       (self.circ_radius, self.circ_radius)))
        draw_circle(target, actual_circ_colour,
                    neg_circ_pos, self.circ_radius)
        draw_rect(target, actual_rect_colour,
                  Rect((neg_circ_pos[0] - self.circ_radius // 2,
                        neg_circ_pos[1] - self.circ_radius // 2),
                       (self.circ_radius, self.circ_radius)))
        target.blit(self.text, (90, 90))
