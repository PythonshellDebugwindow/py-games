import pygame


def set_cursor(cursor: pygame.Cursor | int) -> None:
    """
    pygame.mouse.set_cursor sometimes throws an error for no apparent
    reason; this function wraps the call in a try-except block.

    :param cursor: the new cursor
    """
    try:
        pygame.mouse.set_cursor(cursor)
    except pygame.error:
        print("Caught error:", pygame.error)
