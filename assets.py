"""Contains all the global assets."""

# Standard library imports.
from pathlib import Path

# Third party library imports.
import pygame as pg

# Export the global assets.
__all__ = [
    # Fonts.
    "DEFAULT_FONT",
    # Colors.
    "BLACK",
    "WHITE",
    "GRAY",
    "CYAN",
    "TAN",
    "DARK_TAN",
    # Images.
    "card_images",
    "make_player_button",
    # Misc.
    "ranks_to_pie",
    "VALID_CHARS",
]

# Initialize pygame.
pg.init()

# The default font.
try:
    DEFAULT_FONT = pg.font.Font(str(Path() / "Kenney Future.ttf"), 14)
except (pg.error, FileNotFoundError) as error:
    print(f"Couldn't load font: {error}")
    DEFAULT_FONT = pg.font.Font(None, 20)

# Colors.
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
TAN = (253, 246, 227)
DARK_TAN = (238, 232, 213)

# The button image.
BUTTON_IMG = pg.image.load(str(Path() / "img" / "button.png"))

# The ranks, translated into card images.
ranks_to_pie = {
    "A": "Apple-Pie.png",
    "2": "Cherry-Pie.png",
    "3": "Chocolate-Pie.png",
    "4": "Cutie-Pie.png",
    "5": "Peach-Pie.png",
    "6": "Pecan-Pie.png",
    "7": "Pi-Pie.png",
    "8": "Pie-Chart.png",
    "9": "Pizza-Pie.png",
    "T": "Pumpkin-Pie.png",
    "J": "Python-Pie.png",
    "Q": "Raspberry-Pi.png",
    "K": "Banana-Cream-Pie.png",
}


# Load the card images.
card_images = {}
for card_path in ranks_to_pie.values():
    try:
        card_images[card_path] = pg.image.load(str(Path() / "img" / card_path))
    except pg.error:
        print(f"Error loading image: {card_path}")


# The function to make a player stat button.
def make_player_button(player_id: int, num_cards: int, tricks: list[str]):
    """Returns a Surface for the player stat button.

    player_id: int; the numerical player id

    num_cards: int; number of cards in the player's hand

    tricks: list[str]; a list of strings representing ranks
    """
    # Convert ranks to card image names.
    tricks = [ranks_to_pie[rank].removesuffix(".png") for rank in tricks]
    # Create the line images.
    line_1 = DEFAULT_FONT.render(f"Player {player_id}", True, BLACK)
    line_2 = DEFAULT_FONT.render(f"Cards: {num_cards}", True, BLACK)
    line_3 = DEFAULT_FONT.render("Tricks: " + ", ".join(tricks), True, BLACK)
    # Get the width of the image.
    width = max(line_1.get_width(), line_2.get_width(), line_3.get_width())
    # Create the final image.
    surface = pg.transform.scale(BUTTON_IMG, (width + 10, DEFAULT_FONT.get_height() * 3 + 10)).convert()
    # Blit the lines onto it.
    surface.blit(line_1, (5, 5))
    surface.blit(line_2, (5, DEFAULT_FONT.get_height() + 5))
    surface.blit(line_3, (5, DEFAULT_FONT.get_height() * 2 + 5))
    # Return the button image.
    return surface


# The valid characters for the client address box.
# A dictionary with keys of pygame event codes.
# The tuples represent without and with shift, respectively.
VALID_CHARS = {
    # Alphabet characters.
    pg.K_a: ('a', "A"),
    pg.K_b: ('b', "B"),
    pg.K_c: ('c', "C"),
    pg.K_d: ('d', "D"),
    pg.K_e: ('e', "E"),
    pg.K_f: ('f', "F"),
    pg.K_g: ('g', "G"),
    pg.K_h: ('h', "H"),
    pg.K_i: ('i', "I"),
    pg.K_j: ('j', "J"),
    pg.K_k: ('k', "K"),
    pg.K_l: ('l', "L"),
    pg.K_m: ('m', "M"),
    pg.K_n: ('n', "N"),
    pg.K_o: ('o', "O"),
    pg.K_p: ('p', "P"),
    pg.K_q: ('q', "Q"),
    pg.K_r: ('r', "R"),
    pg.K_s: ('s', "S"),
    pg.K_t: ('t', "T"),
    pg.K_u: ('u', "U"),
    pg.K_v: ('v', "V"),
    pg.K_w: ('w', "W"),
    pg.K_x: ('x', "X"),
    pg.K_y: ('y', "Y"),
    pg.K_z: ('z', "Z"),
    # Numeric characters (with number pad).
    pg.K_0: ('0', "0"),
    pg.K_1: ('1', "1"),
    pg.K_2: ('2', "2"),
    pg.K_3: ('3', "3"),
    pg.K_4: ('4', "4"),
    pg.K_5: ('5', "5"),
    pg.K_6: ('6', "6"),
    pg.K_7: ('7', "7"),
    pg.K_8: ('8', "8"),
    pg.K_9: ('9', "9"),
    pg.K_KP0: ('0', "0"),
    pg.K_KP1: ('1', "1"),
    pg.K_KP2: ('2', "2"),
    pg.K_KP3: ('3', "3"),
    pg.K_KP4: ('4', "4"),
    pg.K_KP5: ('5', "5"),
    pg.K_KP6: ('6', "6"),
    pg.K_KP7: ('7', "7"),
    pg.K_KP8: ('8', "8"),
    pg.K_KP9: ('9', "9"),
    # Punctuation (with number pad).
    pg.K_SEMICOLON: (':', ':'),
    pg.K_PERIOD: ('.', '.'),
    pg.K_KP_PERIOD: ('.', '.'),
}
