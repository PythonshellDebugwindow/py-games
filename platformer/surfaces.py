import pygame

class Platform:
    def __init__(self, x, y, w, h, multiplier=40, is_solid=True):
        self.pos = (x, y)
        self.size = (w * multiplier, h * multiplier)
        self.surf = pygame.Surface((w * multiplier, h * multiplier))
        self.surf.fill((125, 125, 125))
        self.is_solid = is_solid
    def draw(self, screen):
        screen.blit(self.surf, self.pos)
    def is_colliding(self, pos, size):
        return (self.is_solid
            and pos[0] + size[0] > self.pos[0]
            and pos[0] < self.pos[0] + self.size[0]
            and pos[1] + size[1] > self.pos[1]
            and pos[1] + size[1] < self.pos[1] + 10)

class Barrier(Platform):
    def is_colliding(self, pos, size):
        r = self._is_colliding(pos, size)
        if r:
            #Move entity
            pass
        return r
    def _is_colliding(self, pos, size):
        return (pos[0] + size[0] > self.pos[0]
            and pos[0] < self.pos[0] + self.size[0]
            and pos[1] + size[1] > self.pos[1]
            and pos[1] < self.pos[1] + self.size[1])
