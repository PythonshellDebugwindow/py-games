import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 41
        self.h = 95
        self.xspeed = 3
        self.yspeed = 1
        self.is_falling = False
        self.is_jumping = False
        self.health = 3
        self.img = pygame.image.load("assets/images/player.png")
        self.img = pygame.transform.scale(self.img, (self.w, self.h))
    def set_is_falling(self, is_falling):
        self.is_falling = is_falling
        if not self.is_falling:
            self.is_jumping = False
    def lose_health(self):
        self.health -= 1
    def set_health(self, health):
        self.health = health
    def is_dead(self):
        return self.health <= 0
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    def get_xy_wh(self):
        return ((self.x, self.y), (self.w, self.h))
    def update(self):
        yold = self.yspeed
        self.y += yold
        self.yspeed += 0.1
        if not self.is_falling:
            self.y -= yold
            self.yspeed = 0
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
    def move_from_keys(self, keys):
        l = keys[pygame.K_a] or keys[pygame.K_LEFT]
        r = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        self.x += self.xspeed * (r - l)
        if (keys[pygame.K_w]
         or keys[pygame.K_UP]
         or keys[pygame.K_SPACE]):
            self.is_falling = True
        if not self.is_jumping:
            self.yspeed = 0
            self.yspeed += -7.25 * (keys[pygame.K_w]
                                    or keys[pygame.K_UP]
                                    or keys[pygame.K_SPACE])
            self.is_jumping = True
