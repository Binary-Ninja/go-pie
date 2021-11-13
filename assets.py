"""Contains all the global assets."""

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
    # Images.
    "make_player_button",
    "make_card_image",
    # Misc.
    "VALID_CHARS",
]

# Initialize pygame.
pg.init()

# The default font.
DEFAULT_FONT = pg.font.Font(None, 20)

# Colors.
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)


# The function to make a player stat button.
def make_player_button(player_id: int, num_cards: int, tricks: list[str]):
    """Returns a Surface for the player stat button.

    player_id: int; the numerical player id

    num_cards: int; number of cards in the player's hand

    tricks: list[str]; a list of strings representing ranks
    """
    # Create the line images.
    line_1 = DEFAULT_FONT.render(f"Player {player_id}", True, BLACK, GRAY)
    line_2 = DEFAULT_FONT.render(f"Cards: {num_cards}", True, BLACK, GRAY)
    line_3 = DEFAULT_FONT.render("Tricks: " + ", ".join(tricks), True, BLACK, GRAY)
    # Get the width of the image.
    width = max(line_1.get_width(), line_2.get_width(), line_3.get_width())
    # Create the final image.
    surface = pg.Surface((width, DEFAULT_FONT.get_height() * 3)).convert()
    surface.fill(GRAY)
    # Blit the lines onto it.
    surface.blit(line_1, (0, 0))
    surface.blit(line_2, (0, DEFAULT_FONT.get_height()))
    surface.blit(line_3, (0, DEFAULT_FONT.get_height() * 2))
    # Return the button image.
    return surface


# The function to make a card image.
def make_card_image(rank):
    """Returns a Surface for the card image of a given rank."""
    surface = pg.Surface((50, 80)).convert()
    surface.fill(GRAY)
    text = DEFAULT_FONT.render(f"{rank}", True, BLACK, GRAY)
    surface.blit(text, (0, 0))
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
