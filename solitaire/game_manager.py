from math import floor
import random
import sys

import pygame

from button import Button
from card import Card
from colours import DARK_RED, RED
from foundation import Foundation
from main_menu_return_screen import run_main_menu_return_screen
from suit import Suit
from utils import set_cursor
from victory_screen import run_victory_screen


class _GameManager:
    def __init__(self, screen: pygame.Surface):
        self._screen = screen

        size = screen.get_size()
        self._size = size
        self._width, self._height = size

        not_allowed_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(not_allowed_surface, RED, (10, 10), 10, 2)
        pygame.draw.line(not_allowed_surface, RED, (5, 15), (16, 4), 3)
        self._not_allowed_cursor = pygame.Cursor((10, 10), not_allowed_surface)

        self._large_font = pygame.font.SysFont("Arial", 25)
        self._medium_font = pygame.font.SysFont("Arial", 23)
        self._small_font = pygame.font.SysFont("Arial", 18)

        Card.set_font(self._medium_font, self._small_font)
        Foundation.set_fonts(self._large_font, self._small_font)

        redraw_arrow = pygame.image.load("assets/redraw_arrow.svg")
        redraw_arrow = pygame.transform.rotozoom(redraw_arrow, 315, 1)
        redraw_arrow = pygame.transform.smoothscale(redraw_arrow, (32, 32))
        redraw_arrow_rect = redraw_arrow.get_rect(center=(size[0] - 103, 50))
        self._redraw_arrow = redraw_arrow
        self._redraw_outline_rect = (size[0] - 120, 20, 36, 60)
        self._redraw_arrow_rect = redraw_arrow_rect

        self._menu_button = Button(self._screen, "Main Menu",
                                   self._screen.get_height() - 35, 20,
                                   centerx=85)

        self._deck = []
        for suit in Suit:
            for rank in range(13):
                self._deck.append(Card(rank, suit))

        random.shuffle(self._deck)

        self._waste = []

        self._depots = []
        for i in range(1, 8):
            self._depots.append([self._deck.pop() for _ in range(i)])
            self._depots[-1][-1].revealed = True

        # Waste pile
        self._depots.append([])

        self._foundations = {}
        for i, suit in enumerate(Suit):
            self._foundations[suit] = Foundation(suit, (45 + 46 * i, 20))

        self._is_moving_card = False
        self._rank_to_move_from = -1
        self._hovered_rank = -1

        self._should_redraw = True

        self._is_running = True
        self._has_won: bool | None = None

    def run_game(self) -> bool:
        set_cursor(pygame.cursors.arrow)

        while self._is_running:
            self._run_main_loop()

        assert self._has_won is not None
        return self._has_won

    def _run_main_loop(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mousebuttonup()
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mousemotion()

        if self._should_redraw:
            self._draw_game()
            self._should_redraw = False

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            if self._is_moving_card:
                set_cursor(pygame.cursors.arrow)
                self._stop_moving_card()
                self._should_redraw = True

    def _stop_moving_card(self) -> None:
        self._rank_to_move_from = -1
        self._hovered_rank = -1
        self._is_moving_card = False

    def _check_victory(self) -> None:
        if all(foundation.highest_rank == 12
               for foundation in self._foundations.values()):
            self._is_running = False
            self._has_won = True

    def _handle_mousebuttonup(self) -> None:
        self._should_redraw = True

        mouse_pos = pygame.mouse.get_pos()

        if self._menu_button.collidepoint(mouse_pos):
            if run_main_menu_return_screen(self._screen):
                self._is_running = False
                self._has_won = False
            set_cursor(pygame.cursors.arrow)
            return

        if mouse_pos[1] < 80:
            if (self._is_moving_card
                    and mouse_pos[1] >= 20
                    and mouse_pos[0] in range(45, 219)):
                card = self._depots[self._rank_to_move_from][-1]
                foundation = self._foundations[card.suit]
                if card.rank == foundation.get_next_rank():
                    foundation.increment_rank()
                    self._depots[self._rank_to_move_from].pop()
                    self._check_victory()

                    if len(self._depots[self._rank_to_move_from]) > 0:
                        self._depots[self._rank_to_move_from][
                            -1
                        ].revealed = True

                    if self._rank_to_move_from == 7:
                        self._waste.pop()
                        if len(self._waste) > 0:
                            self._depots[7].clear()
                            self._depots[7].append(self._waste[-1])

                    set_cursor(pygame.cursors.arrow)
                    self._stop_moving_card()
                return

            if (mouse_pos[0] in range(self._width - 120, self._width - 83)
                    and mouse_pos[1] in range(20, 80)):
                if len(self._deck) > 0:
                    for _ in range(min(3, len(self._deck))):
                        turned_card = self._deck.pop()
                        turned_card.revealed = True
                        self._waste.append(turned_card)
                    self._depots[7].clear()
                    self._depots[7].append(self._waste[-1])
                else:
                    self._deck = self._waste[::-1]
                    for card in self._deck:
                        card.revealed = False
                    self._waste.clear()
                    self._depots[7].clear()

                self._stop_moving_card()

            elif (mouse_pos[0] in range(self._width - 176, self._width - 140)
                  and mouse_pos[1] in range(20, 80)):
                if self._rank_to_move_from == 7:
                    set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    self._stop_moving_card()
                elif len(self._waste) > 0:
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        card = self._depots[self._rank_to_move_from][-1]
                        foundation = self._foundations[card.suit]
                        if card.rank == foundation.get_next_rank():
                            foundation.increment_rank()
                            self._depots[self._rank_to_move_from].pop()

                            self._check_victory()

                            if len(self._depots[self._rank_to_move_from]) > 0:
                                self._depots[self._rank_to_move_from][
                                    -1
                                ].revealed = True

                            self._waste.pop()

                            self._depots[7].clear()
                            if len(self._waste) > 0:
                                self._depots[7].append(self._waste[-1])

                            self._stop_moving_card()

                        else:
                            set_cursor(self._not_allowed_cursor)

                        return

                    self._hovered_rank = -1
                    self._is_moving_card = True
                    self._rank_to_move_from = 7
                    set_cursor(self._not_allowed_cursor)

            return

        elif mouse_pos[1] < 90 or self._hovered_rank == -1:
            return

        num_cards_in_rank = len(self._depots[self._hovered_rank])
        hovered_rank_bottom = num_cards_in_rank * 27 + 185
        if mouse_pos[1] > hovered_rank_bottom:
            return

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            if len(self._depots[self._hovered_rank]) > 0:
                card = self._depots[self._hovered_rank][-1]
                foundation = self._foundations[card.suit]
                if card.rank == foundation.get_next_rank():
                    foundation.increment_rank()
                    self._depots[self._hovered_rank].pop()

                    self._check_victory()

                    if len(self._depots[self._hovered_rank]) > 0:
                        self._depots[self._hovered_rank][-1].revealed = True
                        set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        set_cursor(pygame.cursors.arrow)

                    self._rank_to_move_from = -1
                    self._is_moving_card = False
                else:
                    set_cursor(self._not_allowed_cursor)
                    self._stop_moving_card()
            else:
                set_cursor(pygame.cursors.arrow)
                self._stop_moving_card()

            return

        if len(self._depots[self._hovered_rank]) == 0:
            if self._is_moving_card:
                card_index = len(self._depots[self._rank_to_move_from]) - 1
                king_to_move = None
                while card_index >= 0:
                    card = self._depots[self._rank_to_move_from][card_index]
                    if not card.revealed:
                        break
                    king_to_move = card
                    card_index -= 1

                if king_to_move and king_to_move.rank == 12:
                    for card in self._depots[self._rank_to_move_from][
                        card_index + 1:
                    ]:
                        self._depots[self._hovered_rank].append(card)
                        self._depots[self._rank_to_move_from].pop()

                    if len(self._depots[self._rank_to_move_from]) > 0:
                        self._depots[self._rank_to_move_from][
                            -1
                        ].revealed = True

                    if self._rank_to_move_from == 7:
                        self._waste.pop()
                        if len(self._waste) > 0:
                            self._depots[7].clear()
                            self._depots[7].append(self._waste[-1])

                    set_cursor(pygame.cursors.arrow)
                    self._stop_moving_card()
            return

        num_cards_to_move = 1

        if self._rank_to_move_from > -1:
            if self._hovered_rank == self._rank_to_move_from:
                set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self._rank_to_move_from = -1
                self._is_moving_card = False
                return

            destination = self._depots[self._hovered_rank][-1]
            card_to_move = self._depots[self._rank_to_move_from][-1]
            can_move = destination.can_be_behind(card_to_move)
            if not can_move:
                i = len(self._depots[self._rank_to_move_from]) - 2
                while i >= 0:
                    num_cards_to_move += 1
                    card = self._depots[self._rank_to_move_from][i]
                    if not card.revealed:
                        break
                    if destination.can_be_behind(card):
                        can_move = True
                        break
                    i -= 1
        else:
            can_move = False

        if self._is_moving_card:
            if can_move:
                moved_cards = []
                for i in range(num_cards_to_move):
                    moved_cards.insert(
                        0, self._depots[self._rank_to_move_from].pop()
                    )
                for card in moved_cards:
                    self._depots[self._hovered_rank].append(card)

                if self._rank_to_move_from == 7:
                    self._waste.pop()
                    if len(self._waste) > 0:
                        self._depots[7].clear()
                        self._depots[7].append(self._waste[-1])

                if len(self._depots[self._rank_to_move_from]) > 0:
                    self._depots[self._rank_to_move_from][-1].revealed = True

                set_cursor(pygame.cursors.arrow)
                self._rank_to_move_from = -1
                self._is_moving_card = False
        else:
            self._rank_to_move_from = self._hovered_rank
            set_cursor(self._not_allowed_cursor)
            self._is_moving_card = True

    def _handle_mousemotion(self) -> None:
        self._should_redraw = True

        mouse_pos = pygame.mouse.get_pos()

        if self._menu_button.collidepoint(mouse_pos):
            set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return

        if (90 <= mouse_pos[1] < self._height - 10
                and 10 <= mouse_pos[0] < self._width - 10):
            self._hovered_rank = floor((mouse_pos[0] - 10) / 75)
            self._hovered_rank = min(6, max(0, self._hovered_rank))
            num_cards_in_rank = len(self._depots[self._hovered_rank])
            hovered_rank_bottom = num_cards_in_rank * 27 + 185
            if mouse_pos[1] > hovered_rank_bottom:
                self._hovered_rank = -1
                set_cursor(pygame.cursors.arrow)
                return
        else:
            self._hovered_rank = -1
            set_cursor(pygame.cursors.arrow)

        if self._is_moving_card and mouse_pos[1] >= 90:
            if len(self._depots[self._hovered_rank]) == 0:
                card_index = len(self._depots[self._rank_to_move_from]) - 1
                king_to_move = None
                while card_index >= 0:
                    card = self._depots[self._rank_to_move_from][card_index]
                    if not card.revealed:
                        break
                    king_to_move = card
                    card_index -= 1

                if king_to_move and king_to_move.rank == 12:
                    set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    set_cursor(pygame.cursors.arrow)
            else:
                destination = self._depots[self._hovered_rank][-1]
                card_to_move = self._depots[self._rank_to_move_from][-1]
                can_move = destination.can_be_behind(card_to_move)
                if not can_move:
                    i = len(self._depots[self._rank_to_move_from]) - 2
                    while i >= 0:
                        card = self._depots[self._rank_to_move_from][i]
                        if not card.revealed:
                            break
                        if destination.can_be_behind(card):
                            can_move = True
                            break
                        i -= 1

                if can_move:
                    set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    set_cursor(self._not_allowed_cursor)
        else:
            if (self._hovered_rank >= 0
                    and mouse_pos[1] >= 90
                    and len(self._depots[self._hovered_rank]) > 0):
                set_cursor(pygame.SYSTEM_CURSOR_HAND)

            elif (self._is_moving_card
                  and mouse_pos[1] >= 20
                  and mouse_pos[0] in range(45, 219)):
                card_to_move = self._depots[self._rank_to_move_from][-1]
                foundation = self._foundations[card_to_move.suit]
                if card_to_move.rank == foundation.get_next_rank():
                    set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    set_cursor(self._not_allowed_cursor)

            elif (mouse_pos[0] in range(self._width - 120, self._width - 83)
                  and mouse_pos[1] in range(20, 80)):
                if len(self._deck) > 0 or len(self._waste) > 0:
                    set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    set_cursor(pygame.cursors.arrow)

            elif (len(self._waste) > 0
                  and mouse_pos[0] in range(self._width - 176,
                                            self._width - 140)
                  and mouse_pos[1] in range(20, 80)):
                if self._rank_to_move_from == 7:
                    set_cursor(self._not_allowed_cursor)
                else:
                    set_cursor(pygame.SYSTEM_CURSOR_HAND)

            else:
                set_cursor(pygame.cursors.arrow)

    def _draw_game(self) -> None:
        self._screen.fill(RED)

        self._menu_button.draw(pygame.mouse.get_pos())

        if self._rank_to_move_from > -1:
            if self._rank_to_move_from < 7:
                num_cards_in_rank = len(self._depots[self._rank_to_move_from])
                hovered_rect_height = num_cards_in_rank * 27 + 95
                hovered_rank_rect = (10 + 75 * self._rank_to_move_from, 90,
                                     80, hovered_rect_height)
            else:
                hovered_rank_rect = (self._width - 183, 12, 51, 76)
            pygame.draw.rect(self._screen, (75, 0, 0), hovered_rank_rect)

        for i, suit in enumerate(Suit):
            self._foundations[suit].draw(self._screen)

        for i in range(7):
            for j, card in enumerate(self._depots[i]):
                card.draw(self._screen, (20 + 75 * i, 100 + 27 * j))

        if len(self._deck) > 0:
            self._deck[-1].draw_small(self._screen, (self._width - 120, 20))
        elif len(self._waste) > 0:
            self._screen.fill(DARK_RED, self._redraw_outline_rect)
            self._screen.blit(self._redraw_arrow, self._redraw_arrow_rect)

        if len(self._waste) > 0:
            self._waste[-1].draw_small(self._screen, (self._width - 176, 20))

        pygame.display.flip()


def run_game(screen: pygame.Surface) -> None:
    if _GameManager(screen).run_game():
        run_victory_screen(screen)
