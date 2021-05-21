import pygame

"""
    Maze class: holds walls for a Pacman maze
    IMPORTANT: Only use straight walls:
               (100,100,100,300) is fine, but not (100,100,300,300)
    IMPORTANT: Put the point which is closer to the origin (0,0) first:
               (100,100,100,300) is fine, but not (100,300,100,100)
"""
class Maze:
    def __init__(self):
        self.walls = []
        s = open("assets/WALLS.txt").read()
        for l in map(str.split, s.split("\n")):
            self.walls.append((int(l[0]), int(l[1]), int(l[2]), int(l[3])))
    def draw(self, screen):
        for l in self.walls:
            pygame.draw.line(screen, (255, 255, 255), l[:2], l[2:])
    def is_colliding(self, pos, size):
        for l in self.walls:
            a = 0 if l[1] == l[3] else 1
            if (pos[a] + size / 2 >= l[a]
                and pos[a] + size / 2 <= l[a + 2]
                and pos[1 - a] + size / 2 >= l[a + 1]
                and pos[1 - a] + size / 2 <= l[a + 1]):
                return True
        return False
