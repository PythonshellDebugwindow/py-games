import pygame
from engine.behaviour import Behaviour

class ScreenshotTaker(Behaviour):
    def __init__(self):
        super().__init__()
        self.num_screenshots=int(open("assets/txt/NUM_SCREENSHOTS.txt").read())
        self.activation_key = "LSHIFT"

    def start(self):
        super().start()
        self.activation_key = getattr(pygame, "K_" + self.activation_key)
    
    def render(self):
        super().render()

    def update(self):
        super().update()
        if pygame.key.get_pressed()[self.activation_key]:
            self.screenshot()
    
    def screenshot(self):
        self.num_screenshots += 1
        path = "Screenshots/Screenshot " + str(self.num_screenshots) + ".png"
        surf = pygame.display.get_surface()
        pygame.image.save(surf, path)

        fl = open("assets/txt/NUM_SCREENSHOTS.txt", "w")
        fl.write(str(self.num_screenshots))
        fl.close()
