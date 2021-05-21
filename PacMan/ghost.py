import pygame, random

class Ghost:
    def __init__(self, pos, _dir, img_path):
        self.pos = pos
        self.dir = _dir
        self.speed = 20
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (40, 40))
        self.img_pellet = pygame.image.load("assets/ghost-pellet.png")
        self.img_pellet = self.img_pellet.convert_alpha()
        self.img_pellet = pygame.transform.scale(self.img_pellet, (40, 40))
    def move(self, maze):
        if self.dir == 0:
            self.pos[1] -= self.speed
        elif self.dir == 1:
            self.pos[0] += self.speed
        elif self.dir == 2:
            self.pos[1] += self.speed
        elif self.dir == 3:
            self.pos[0] -= self.speed
        
        if maze.is_colliding(self.pos, 40): #or random.randint(0, 19) == 0:
            if self.dir == 0:
                self.pos[1] += self.speed
            elif self.dir == 1:
                self.pos[0] -= self.speed
            elif self.dir == 2:
                self.pos[1] -= self.speed
            elif self.dir == 3:
                self.pos[0] += self.speed
            
            self.dir = random.randint(0, 3)
        
        if self.pos[0] < 0:
            self.pos[0] = 800
        elif self.pos[0] > 800:
            self.pos[0] = 0
    def draw(self, surf, pacman_has_pellet):
        surf.blit(self.img_pellet if pacman_has_pellet else self.img, self.pos)
    def is_colliding(self, pos, size):
        return (self.pos[0] - 40 <= pos[0] - size / 2
            and self.pos[0] + 40 >= pos[0] + size / 2
            and self.pos[1] - 40 <= pos[1] - size / 2
            and self.pos[1] + 40 >= pos[1] + size / 2)
