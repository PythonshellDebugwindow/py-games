import sys

import pygame

from button import Button
from colours import BLACK, RED
from utils import set_cursor


class _TitleScreen:
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._width, self._height = screen.get_size()

        title_font = pygame.font.SysFont("Arial", 70)

        self._title_text = title_font.render("Solitaire", True, BLACK)
        title_center = (self._width // 2, self._height // 2 - 120)
        self._title_text_rect = self._title_text.get_rect(center=title_center)

        self._start_button = Button(self._screen, "Start Game",
                                    self._height // 2 - 30)

        self._help_button = Button(self._screen, "Help",
                                   self._height // 2 + 55,
                                   width=self._start_button.get_width())

        self._exit_button = Button(self._screen, "Exit",
                                   self._height // 2 + 140,
                                   width=self._start_button.get_width())

        self._draw_title_screen()

        self._is_running = True
        self._will_run_game: bool | None = None

    def run_title_screen(self) -> bool:
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._handle_mousebuttonup()
                elif event.type == pygame.MOUSEMOTION:
                    self._draw_title_screen()

        assert self._will_run_game is not None
        return self._will_run_game

    def _handle_mousebuttonup(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self._start_button.collidepoint(mouse_pos):
            self._is_running = False
            self._will_run_game = True
        elif self._help_button.collidepoint(mouse_pos):
            _HelpScreen(self._screen).run_help_screen()
            self._draw_title_screen()
        elif self._exit_button.collidepoint(mouse_pos):
            self._is_running = False
            self._will_run_game = False

    def _draw_title_screen(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        self._screen.fill(RED)
        self._screen.blit(self._title_text, self._title_text_rect)

        self._start_button.draw(mouse_pos)
        self._help_button.draw(mouse_pos)
        self._exit_button.draw(mouse_pos)

        if (self._start_button.collidepoint(mouse_pos)
                or self._help_button.collidepoint(mouse_pos)
                or self._exit_button.collidepoint(mouse_pos)):
            set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            set_cursor(pygame.cursors.arrow)

        pygame.display.flip()


class _HelpScreen:
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._width, self._height = screen.get_size()

        title_font = pygame.font.SysFont("Arial", 60)
        text_font = pygame.font.SysFont("Arial", 22)

        self._title_text = title_font.render("Instructions", True, BLACK)
        title_center = (self._width // 2, 60)
        self._title_text_rect = self._title_text.get_rect(center=title_center)

        rules_messages = [
            "A game of standard Klondike solitaire. Move all",
            "cards to the four foundations in the top left to win!",
            "",
            "To move a card, first click on its rank to select it,",
            "then click the rank or card onto which to move it.",
            "Clicking the deck in the top right draws three cards,",
            "or fewer if there are only one or two cards left.",
            "",
            "Shift-clicking a card automatically moves it to its",
            "suit's foundation if that would be a valid move.",
            "Pressing the Escape key cancels a move, as does",
            "clicking on the same rank again."
        ]
        self._rules_texts = [text_font.render(message, True, BLACK)
                             for message in rules_messages]
        rules_centers = [(self._width // 2, 125 + i * 31)
                         for i in range(len(rules_messages))]
        self._rules_text_rects = [
            text.get_rect(center=center)
            for text, center in zip(self._rules_texts, rules_centers)
        ]

        self._back_button = Button(self._screen, "Back",
                                   self._height // 2 + 230, width=208)

        self._draw_help_screen()

        self._is_running = True

    def run_help_screen(self) -> None:
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._handle_mousebuttonup()
                elif event.type == pygame.MOUSEMOTION:
                    self._draw_help_screen()

    def _handle_mousebuttonup(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self._back_button.collidepoint(mouse_pos):
            self._is_running = False

    def _draw_help_screen(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        self._screen.fill(RED)
        self._screen.blit(self._title_text, self._title_text_rect)

        for text, rect in zip(self._rules_texts, self._rules_text_rects):
            self._screen.blit(text, rect)

        self._back_button.draw(mouse_pos)

        if self._back_button.collidepoint(mouse_pos):
            set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            set_cursor(pygame.cursors.arrow)

        pygame.display.flip()


def run_title_screen(screen: pygame.Surface) -> bool:
    return _TitleScreen(screen).run_title_screen()
