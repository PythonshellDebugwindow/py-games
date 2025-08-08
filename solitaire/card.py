from __future__ import annotations

from pygame import Rect, Surface
from pygame.font import Font

from colours import WHITE, BLACK, RED, DARK_RED
from suit import Suit

rank_symbols = [
    "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
]


class Card:
    _font: Font | None = None
    _small_font: Font | None = None
    _s_text: Surface | None = None
    _s_text_small: Surface | None = None

    def __init__(self, rank: int, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.revealed = False
        self._is_black = suit == Suit.CLUBS or suit == Suit.SPADES

        text = rank_symbols[rank] + suit.value
        text_colour = BLACK if self._is_black else RED
        self._rank_text = Card._font.render(text, True, text_colour)
        self._rank_text_small = Card._small_font.render(text, True, text_colour)

    def draw(self, screen: Surface, position: tuple[int, int]) -> None:
        rect = Rect(position, (60, 100))
        if self.revealed:
            screen.fill(WHITE, rect)
            screen.blit(self._rank_text, rect.move(2, 1))
        else:
            screen.fill(DARK_RED, rect)
            screen.blit(Card._s_text, rect.move(2, 1))

    def draw_small(self, screen: Surface, position: tuple[int, int]) -> None:
        rect = Rect(position, (36, 60))
        if self.revealed:
            screen.fill(WHITE, rect)
            screen.blit(self._rank_text_small, rect.move(2, 1))
        else:
            screen.fill(DARK_RED, rect)
            screen.blit(Card._s_text_small, rect.move(2, 1))

    def can_be_behind(self, other: Card) -> bool:
        return (self._is_black != other._is_black
                and self.rank - 1 == other.rank)

    @classmethod
    def set_font(cls, font: Font, small_font: Font) -> None:
        cls._font = font
        cls._small_font = small_font
        cls._s_text = font.render("S", True, RED)
        cls._s_text_small = small_font.render("S", True, RED)
