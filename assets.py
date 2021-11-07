"""Contains all the global assets."""

# Third party library imports.
import pygame as pg

# Export the global assets.
__all__ = [
    "DEFAULT_FONT",
    "BLACK",
    "WHITE",
    "GRAY",
]

# Initialize pygame.
pg.init()

# The default font.
DEFAULT_FONT = pg.font.Font(None, 20)

# Colors.
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
