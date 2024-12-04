import pygame

def get_font(size):
    """
    Get a Pygame font object with a specified size.

    Parameters
    ----------
    size : int
        The font size.

    Returns
    -------
    pygame.font.Font
        A Pygame font object.
    """

    return pygame.font.Font(r"assets/font.ttf", size)


font = get_font(12)
