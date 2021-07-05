from random import randrange
from pygame import Surface, Color

class Collectible:
    def __init__(self, size, max_cells):
        self.started = False
        self.max_cells = max_cells
        self.cur_cell = (0, 0)
        self.surf = Surface(size)
        self.rect = self.surf.get_rect()

        colorkey = Color(0, 255, 0)
        fruit_colour = Color(217, 14, 24)
        self.surf.fill(colorkey)

        from pygame.draw import circle
        
        circle(self.surf, fruit_colour, self.rect.center,
               self.rect.width // 2 - 1)
        self.surf.set_colorkey(colorkey)
        
        self.reposition()
    def start(self):
        self.started = self.surf != None and self.surf.get_colorkey() != None
        return self.started
    def update(self, delta):
        pass
    def render(self, target):
        target.blit(self.surf, self.rect)
    def reposition(self):
        self.cur_cell = (randrange(0, self.max_cells),
                         randrange(0, self.max_cells))
        self.rect.left = self.cur_cell[0] * self.rect.width
        self.rect.top = self.cur_cell[1] * self.rect.height
    def get_current_cell(self):
        return self.cur_cell
