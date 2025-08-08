import sys

import pygame

from button import Button
from colours import BLACK, RED
from utils import set_cursor


class _VictoryScreen:
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._width, self._height = screen.get_size()

        title_font = pygame.font.SysFont("Arial", 70)

        self._title_text = title_font.render("You Win!", True, BLACK)
        title_center = (self._width // 2, self._height // 2 - 50)
        self._title_text_rect = self._title_text.get_rect(center=title_center)

        self._return_button = Button(self._screen, "Main Menu",
                                     self._height // 2 + 50)

        self._draw_victory_screen()

        self._is_running = True

    def run_victory_screen(self) -> None:
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._handle_mousebuttonup()
                elif event.type == pygame.MOUSEMOTION:
                    self._draw_victory_screen()

    def _handle_mousebuttonup(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self._return_button.collidepoint(mouse_pos):
            self._is_running = False

    def _draw_victory_screen(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        self._screen.fill(RED, (0, 80, self._width, self._height - 80))
        self._screen.blit(self._title_text, self._title_text_rect)

        self._return_button.draw(mouse_pos)

        if self._return_button.collidepoint(mouse_pos):
            set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            set_cursor(pygame.cursors.arrow)

        pygame.display.flip()


def run_victory_screen(screen: pygame.Surface) -> None:
    _VictoryScreen(screen).run_victory_screen()
