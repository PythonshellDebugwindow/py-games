import sys

import pygame

from button import Button
from colours import BLACK
from utils import set_cursor


class _MainMenuReturnScreen:
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._width, self._height = screen.get_size()

        self._dialogue_rect = (self._width // 2 - 150, self._height // 2 - 67,
                               300, 134)

        text_font = pygame.font.SysFont("Arial", 24)
        texts = [
            "Stop this game and go",
            "back to the main menu?"
        ]
        self._texts = [text_font.render(text, True, BLACK) for text in texts]
        self._text_rects = [
            text.get_rect(center=(self._width // 2,
                                  self._height // 2 - 43 + i * 30))
            for i, text in enumerate(self._texts)
        ]

        self._ok_button = Button(self._screen, "Go Back",
                                 self._height // 2 + 32,
                                 font_size=20,
                                 centerx=self._width // 2 - 65)

        self._cancel_button = Button(self._screen, "Cancel",
                                     self._height // 2 + 32,
                                     font_size=20,
                                     width=self._ok_button.get_width(),
                                     centerx=self._width // 2 + 65)

        self._is_running = True
        self._result: bool | None = None

        self._draw_dialogue()

    def run_confirm_dialogue(self) -> bool:
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._handle_mousebuttonup()
                elif event.type == pygame.MOUSEMOTION:
                    self._draw_dialogue()

        assert self._result is not None
        return self._result

    def _handle_mousebuttonup(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self._ok_button.collidepoint(mouse_pos):
            self._is_running = False
            self._result = True
        elif self._cancel_button.collidepoint(mouse_pos):
            self._is_running = False
            self._result = False

    def _draw_dialogue(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(self._screen, (130, 130, 130), self._dialogue_rect)
        pygame.draw.rect(self._screen, BLACK, self._dialogue_rect, 2)

        for text, rect in zip(self._texts, self._text_rects):
            self._screen.blit(text, rect)

        self._ok_button.draw(mouse_pos)
        self._cancel_button.draw(mouse_pos)

        if (self._ok_button.collidepoint(mouse_pos)
                or self._cancel_button.collidepoint(mouse_pos)):
            set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            set_cursor(pygame.cursors.arrow)

        pygame.display.flip()


def run_main_menu_return_screen(screen: pygame.Surface) -> bool:
    return _MainMenuReturnScreen(screen).run_confirm_dialogue()
