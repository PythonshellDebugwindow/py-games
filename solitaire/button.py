import pygame

from colours import BLACK


class Button:
    _fonts: dict[int, pygame.font.Font] = {}

    def __init__(self, screen: pygame.Surface, text: str, centery: int,
                 font_size: int = 35, width: int = None, centerx: int = None):
        self._screen = screen

        if font_size not in Button._fonts:
            Button._fonts[font_size] = pygame.font.SysFont("Arial", font_size)
        self._text = Button._fonts[font_size].render(text, True, BLACK)
        text_center_x = screen.get_width() // 2 if centerx is None else centerx
        self._text_rect = self._text.get_rect(center=(text_center_x, centery))

        self._button_rect = self._text_rect.inflate(30, 20)
        if width is not None:
            self._button_rect.width = width
            self._button_rect.centerx = text_center_x

    def draw(self, mouse_pos: tuple[int, int]) -> None:
        help_colour = self._get_colour(mouse_pos)
        pygame.draw.rect(self._screen, help_colour, self._button_rect)
        pygame.draw.rect(self._screen, BLACK, self._button_rect, 2)
        self._screen.blit(self._text, self._text_rect)

    def collidepoint(self, mouse_pos: tuple[int, int]) -> bool:
        return self._button_rect.collidepoint(mouse_pos)

    def get_width(self) -> int:
        return self._button_rect.width

    def _get_colour(self, mouse_pos: tuple[int, int]) -> tuple[int, int, int]:
        if self.collidepoint(mouse_pos):
            return (125, 125, 125)
        else:
            return (175, 175, 175)
