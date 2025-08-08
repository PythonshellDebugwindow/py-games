from pygame import Surface
from pygame.font import Font

from card import rank_symbols
from colours import WHITE, BLACK, RED, DARK_RED
from suit import Suit


class Foundation:
    _medium_font: Font | None = None
    _small_font: Font | None = None

    def __init__(self, suit: Suit, position: tuple[int, int]):
        self.suit = suit
        self.highest_rank: int | None = None
        self._position = position
        self._size_and_position = (position, (36, 60))

        is_black = (suit == Suit.CLUBS or suit == Suit.SPADES)
        self._colour = BLACK if is_black else RED

        self._background_colour = DARK_RED

        self._rank_text = Foundation._medium_font.render(suit.value, True, BLACK)

        text_center = (self._position[0] + 17, self._position[1] + 28)
        self._rank_text_rect = self._rank_text.get_rect(center=text_center)

    def draw(self, screen: Surface) -> None:
        screen.fill(self._background_colour, self._size_and_position)
        screen.blit(self._rank_text, self._rank_text_rect)

    def get_next_rank(self) -> int:
        if self.highest_rank is None:
            return 0
        else:
            return self.highest_rank + 1

    def increment_rank(self) -> None:
        if self.highest_rank is None:
            self.highest_rank = 0
            self._background_colour = WHITE
        else:
            self.highest_rank += 1

        text = rank_symbols[self.highest_rank] + self.suit.value
        new_text = Foundation._small_font.render(text, True, self._colour)
        self._rank_text = new_text
        rank_text_pos = (self._position[0] + 2, self._position[1] + 1)
        self._rank_text_rect = (rank_text_pos, (36, 60))

    @classmethod
    def set_fonts(cls, medium_font: Font, small_font: Font) -> None:
        cls._medium_font = medium_font
        cls._small_font = small_font
