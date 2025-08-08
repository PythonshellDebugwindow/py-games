import pygame

from game_manager import run_game
from title_screen import run_title_screen


def main() -> None:
    pygame.init()

    size = 550, 620
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Solitaire")

    while run_title_screen(screen):
        run_game(screen)


if __name__ == "__main__":
    main()
