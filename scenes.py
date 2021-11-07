"""The file to contain all scene classes."""

# Third party library imports.
import pygame as pg

# Local library imports.
from assets import *

# Export the scenes.
__all__ = [
    "StartScene",
    "HostScene",
]


class BaseScene:
    """The base class for a scene. Should not be instantiated."""

    # The scene to switch to next.
    next_scene = None

    def pump(self):
        """Pump network classes in the scene."""

    def events(self, events):
        """Handle pygame events."""

    def update_screen_size(self, screen_rect):
        """Updates scene based on new screen size."""

    def update(self, dt):
        """Update everything in the scene."""

    def draw(self, screen):
        """Draw everything in the scene."""


class StartScene(BaseScene):
    """The first scene the user sees.

    Gives the option to either host or join a server.
    """
    def __init__(self, screen_rect):
        """Requires the Rect of the display screen."""
        # Create the button images.
        self.host_button_img = DEFAULT_FONT.render("(H)ost Server", True, BLACK, GRAY)
        self.join_button_img = DEFAULT_FONT.render("(J)oin Server", True, BLACK, GRAY)
        # Get the button rectangles.
        self.host_button_rect = self.host_button_img.get_rect()
        self.join_button_rect = self.join_button_img.get_rect()
        # Place the buttons on the screen.
        self.place_buttons(screen_rect)

    def place_buttons(self, screen_rect):
        """Places the buttons in their proper place on screen."""
        self.host_button_rect.centerx = screen_rect.centerx
        self.join_button_rect.centerx = screen_rect.centerx
        self.host_button_rect.centery = screen_rect.centery - self.host_button_rect.height - 10
        self.join_button_rect.centery = screen_rect.centery + 10

    def update_screen_size(self, screen_rect):
        self.place_buttons(screen_rect)

    def events(self, events):
        """Handle pygame events."""
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_h:
                    self.next_scene = "host"
                elif event.key == pg.K_j:
                    self.next_scene = "join"
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check for button clicks.
                    if self.host_button_rect.collidepoint(event.pos):
                        self.next_scene = "host"
                    elif self.join_button_rect.collidepoint(event.pos):
                        self.next_scene = "join"

    def draw(self, screen):
        screen.blit(self.host_button_img, self.host_button_rect)
        screen.blit(self.join_button_img, self.join_button_rect)


class HostScene(BaseScene):
    """The server creation scene.

    Contains all the server config options.
    """
    def __init__(self, screen_rect):
        """Requires the Rect of the display screen."""
        # Create the button images.
        self.start_button_img = DEFAULT_FONT.render("(ENTER) Start Server", True, BLACK, GRAY)
        self.back_button_img = DEFAULT_FONT.render("(ESC) Main Menu", True, BLACK, GRAY)
        # Get the button rectangles.
        self.start_button_rect = self.start_button_img.get_rect()
        self.back_button_rect = self.back_button_img.get_rect()
        # Place the buttons on the screen.
        self.place_buttons(screen_rect)

    def place_buttons(self, screen_rect):
        """Places the buttons in their proper place on screen."""
        self.start_button_rect.centery = screen_rect.centery
        self.back_button_rect.centery = screen_rect.centery
        self.start_button_rect.x = screen_rect.centerx + 10
        self.back_button_rect.x = screen_rect.centerx - self.back_button_rect.width - 10

    def update_screen_size(self, screen_rect):
        self.place_buttons(screen_rect)

    def events(self, events):
        """Handle pygame events."""
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_RETURN:
                    self.next_scene = "game"
                elif event.key == pg.K_ESCAPE:
                    self.next_scene = "start"
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check for button clicks.
                    if self.start_button_rect.collidepoint(event.pos):
                        self.next_scene = "game"
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.next_scene = "start"

    def draw(self, screen):
        screen.blit(self.start_button_img, self.start_button_rect)
        screen.blit(self.back_button_img, self.back_button_rect)
