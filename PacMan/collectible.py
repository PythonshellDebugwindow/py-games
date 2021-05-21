import pygame

_COLLECTIBLE_IMG_PATHS = {
    "fruit": "assets/cherry.png",
    "pac-dot": "assets/pac-dot.png",
    "pac-pellet": "assets/pac-dot.png"
}

class Collectible:
    def __init__(self, _type, img_path, pos, size):
        self.type = _type
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, size)
        self.real_pos = pos
        self.draw_pos = (self.real_pos[0] + (40 - size[0]) / 2,
                         self.real_pos[1] + (40 - size[1]) / 2)
    def draw(self, screen):
        screen.blit(self.img, self.draw_pos)
    def is_colliding(self, pos):
        return self.real_pos[0] == pos[0] and self.real_pos[1] == pos[1]
    @staticmethod
    def get_collectibles():
        c = []
        for l in open("assets/COLLECTIBLES.txt").read().split("\n"):
            sl = l.split()
            c.append(Collectible(sl[0], _COLLECTIBLE_IMG_PATHS[sl[0]],
                                 (int(sl[1]), int(sl[2])),
                                 (int(sl[3]), int(sl[4]))))
        return c
