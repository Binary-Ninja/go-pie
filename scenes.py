"""The file to contain all scene classes."""

# Standard library imports.
from enum import Enum, auto

# Third party library imports.
import pygame as pg

# Local library imports.
from config import *
from assets import *


class NextScene(Enum):
    """A simple Enum for scene transition values."""
    QUIT = auto()
    START = auto()
    HOST = auto()
    JOIN = auto()
    GAME = auto()


class Widget:
    """A basic widget that holds an image and a rectangle."""
    def __init__(self, image: pg.Surface):
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, screen: pg.Surface):
        """Draws the widget on the given surface."""
        screen.blit(self.image, self.rect)


class BaseScene:
    """The base class for a scene. Should not be instantiated."""

    # The scene to switch to next.
    next_scene = None

    def __init__(self, screen_rect):
        """Remember the screen_rect for future updates."""
        self.screen_rect = screen_rect

    def pump(self):
        """Pump network classes in the scene."""

    def events(self, events):
        """Handle pygame events."""

    def update_screen_size(self, screen_rect):
        """Updates scene based on new screen size."""
        self.screen_rect = screen_rect

    def update(self, dt):
        """Update everything in the scene."""

    def draw(self, screen):
        """Draw everything in the scene."""


class StartScene(BaseScene):
    """The first scene the user sees.

    Gives the option to either host or join a server.
    """
    def __init__(self, screen_rect):
        super().__init__(screen_rect)
        # Create the widgets.
        self.host_button = Widget(DEFAULT_FONT.render("(H)ost Server", True, BLACK, GRAY))
        self.join_button = Widget(DEFAULT_FONT.render("(J)oin Server", True, BLACK, GRAY))
        # Position the widgets on the screen.
        self.position_widgets()

    def position_widgets(self):
        """Places the widgets in their proper place on screen."""
        self.host_button.rect.centerx = self.screen_rect.centerx
        self.join_button.rect.centerx = self.screen_rect.centerx
        self.host_button.rect.centery = self.screen_rect.centery - self.host_button.rect.height - 10
        self.join_button.rect.centery = self.screen_rect.centery + 10

    def update_screen_size(self, screen_rect):
        self.screen_rect = screen_rect
        self.position_widgets()

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_ESCAPE:
                    self.next_scene = NextScene.QUIT
                elif event.key == pg.K_h:
                    self.next_scene = NextScene.HOST
                elif event.key == pg.K_j:
                    self.next_scene = NextScene.JOIN
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check for button clicks.
                    if self.host_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.HOST
                    elif self.join_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.JOIN

    def draw(self, screen):
        self.host_button.draw(screen)
        self.join_button.draw(screen)


class HostScene(BaseScene):
    """The server creation scene.

    Contains all the server config options.
    """
    def __init__(self, screen_rect):
        super().__init__(screen_rect)
        # Create the widgets.
        self.start_button = Widget(DEFAULT_FONT.render("(ENTER) Start Server", True, BLACK, GRAY))
        self.back_button = Widget(DEFAULT_FONT.render("(ESC) Main Menu", True, BLACK, GRAY))
        # Position the widgets on the screen.
        self.position_widgets()

    def position_widgets(self):
        """Places the widgets in their proper place on screen."""
        self.start_button.rect.centery = self.screen_rect.centery
        self.back_button.rect.centery = self.screen_rect.centery
        self.start_button.rect.x = self.screen_rect.centerx + 10
        self.back_button.rect.x = self.screen_rect.centerx - self.back_button.rect.width - 10

    def update_screen_size(self, screen_rect):
        self.screen_rect = screen_rect
        self.position_widgets()

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_RETURN:
                    self.next_scene = NextScene.GAME
                elif event.key == pg.K_ESCAPE:
                    self.next_scene = NextScene.START
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check for button clicks.
                    if self.start_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.GAME
                    elif self.back_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.START

    def draw(self, screen):
        self.start_button.draw(screen)
        self.back_button.draw(screen)


class JoinScene(BaseScene):
    """The join server scene.

    Contains a text box to enter the server address.
    """
    def __init__(self, screen_rect):
        super().__init__(screen_rect)
        # Create the widgets.
        self.start_button = Widget(DEFAULT_FONT.render("(ENTER) Join Server", True, BLACK, GRAY))
        self.back_button = Widget(DEFAULT_FONT.render("(ESC) Main Menu", True, BLACK, GRAY))
        # Create the text box.
        self.text = f"{DEFAULT_HOST}:{DEFAULT_PORT}"
        self.text_box = Widget(DEFAULT_FONT.render("Address: " + self.text, True, BLACK, GRAY))
        # Position the widgets on the screen.
        self.position_widgets()

    def position_widgets(self):
        """Places the widgets in their proper place on screen."""
        # Place the buttons.
        self.start_button.rect.centery = self.screen_rect.centery
        self.back_button.rect.centery = self.screen_rect.centery
        self.start_button.rect.x = self.screen_rect.centerx + 10
        self.back_button.rect.x = self.screen_rect.centerx - self.back_button.rect.width - 10
        # Place the text box.
        self.text_box.rect.centerx = self.screen_rect.centerx
        self.text_box.rect.bottom = self.screen_rect.centery - self.start_button.rect.height

    def update_text_box(self):
        """Updates the text box after text has been changed."""
        self.text_box = Widget(DEFAULT_FONT.render("Address: " + self.text, True, BLACK, GRAY))
        # Position the text box.
        self.text_box.rect.centerx = self.screen_rect.centerx
        self.text_box.rect.bottom = self.screen_rect.centery - self.start_button.rect.height

    def update_screen_size(self, screen_rect):
        self.screen_rect = screen_rect
        self.position_widgets()

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_RETURN:
                    self.next_scene = NextScene.GAME
                elif event.key == pg.K_ESCAPE:
                    self.next_scene = NextScene.START
                elif event.key == pg.K_BACKSPACE:
                    # If there is text, delete one character.
                    if self.text:
                        self.text = self.text[:-1]
                    self.update_text_box()
                elif event.key == pg.K_DELETE:
                    # Clear the text box.
                    self.text = ""
                    self.update_text_box()
                elif event.key in VALID_CHARS:
                    # Add one character to the text, taking into account the shift key.
                    self.text += VALID_CHARS[event.key][bool(event.mod & pg.KMOD_SHIFT)]
                    self.update_text_box()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check for button clicks.
                    if self.start_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.GAME
                    elif self.back_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.START

    def draw(self, screen):
        self.start_button.draw(screen)
        self.back_button.draw(screen)
        self.text_box.draw(screen)
