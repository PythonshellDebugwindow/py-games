from pygame import Color, Rect, Surface, K_SPACE, K_p
from pygame.draw import rect as draw_rect, circle as draw_circle
from pygame.key import get_pressed as get_pressed_keys
from pygame.font import SysFont

from src.collectible import Collectible
from src.snake import Snake

class Scene:
    def __init__(self):
        self.started = False

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
        self.score = 0
        self.snake = Snake(self.cell_size, self.cell_amt)
        self.snake_is_dead = False
        
        self.draw_checkerboard()
        
        self.font = SysFont("Arial", 30)
        self.text = self.font.render("Score: 0", False, self.back_colour)
    
    def draw_checkerboard(self):
        for i in range(self.cell_amt):
            for j in range(self.cell_amt):
                if (i % 2 == 0) ^ (j % 2 == 0):
                    cr = Rect((i * self.cell_size[0], j * self.cell_size[1]),
                              self.cell_size)
                    draw_rect(self.play_surf, self.cell_colour, cr)
    
    def start(self):
        self.fruit.start()
        self.snake.start()
        self.started = True
        return self.started
    
    def update(self, delta):
        if not self.snake_is_dead:
            if get_pressed_keys()[K_SPACE]:
                self.fruit.reposition()
            elif get_pressed_keys()[K_p]:
                self.snake.set_growth()
                self.handle_collected()
                self.snake.move()
            
            self.fruit.update(delta)
            self.collect()
            self.snake.update(delta)
            if not self.snake.check_alive():
                self.snake_is_dead = True
                self.text = self.font.render(f"Game Over",
                                             False, self.back_colour)
    
    def render(self, target):
        target.fill(self.bg_colour)
        
        if not self.snake_is_dead:
            target.blit(self.play_surf, self.play_rect)
            self.fruit.render(target)
            self.snake.render(target)
            target.blit(self.text, (560, 90))
        else:
            target.blit(self.text, (90, 90))

    def collect(self):
        if self.fruit.get_current_cell() == self.snake.get_head():
            self.snake.set_growth()
            snake_pos = self.snake.get_snake()
            while self.fruit.get_current_cell() in snake_pos:
                self.fruit.reposition()
            self.handle_collected()
    
    def handle_collected(self):
        self.score += 1
        if self.score % 5 == 0:
            self.snake.speed_change = True
        self.text = self.font.render(f"Score: {self.score}",
                                     False, self.back_colour)
