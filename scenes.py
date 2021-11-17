"""The file to contain all scene classes."""

# Standard library imports.
from enum import Enum, auto

# Third party library imports.
import pygame as pg
from pygame.math import Vector2

# Import ngrok if available.
try:
    from pyngrok import ngrok
except ImportError:
    ngrok = None
    print("WARNING: Public server creation unavailable.")

# Local library imports.
from config import *
from assets import *

from server import PieServer
from client import PieClient


class Particle(pg.sprite.Sprite):
    def __init__(self, pos, size, angle=0, pos_vel=0, angle_vel=0):
        super().__init__()
        # Whether the particle is dead or not.
        self.dead = False
        # Store the particle state.
        self.pos = Vector2(pos)
        self.angle = angle
        self.pos_vel = Vector2(pos_vel)
        self.angle_vel = angle_vel
        # Create the base image.
        self.base_image = pg.Surface(size).convert()
        self.base_image.fill(DARK_TAN)
        self.base_image.set_colorkey(BLACK)
        # Create the main image.
        self.image = pg.transform.rotate(self.base_image, self.angle)
        # Create the rect.
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, dt):
        # Update the particle state.
        # Convert units per tick to units per second.
        self.pos += self.pos_vel * dt / 1000
        self.angle += self.angle_vel * dt / 1000
        # Wrap angle around unit circle.
        self.angle %= 360

        # Create a new image.
        self.image = pg.transform.rotate(self.base_image, int(self.angle))
        # Reposition the drawing rectangle.
        self.rect = self.image.get_rect()
        self.rect.center = int(self.pos.x), int(self.pos.y)


class NextScene(Enum):
    """A simple Enum for scene transition values."""
    QUIT = auto()
    START = auto()
    HOST = auto()
    JOIN = auto()
    GAME = auto()


class Widget:
    """A basic widget that holds an image and a rectangle."""
    def __init__(self, image: pg.Surface, data=None):
        self.image = image
        self.rect = self.image.get_rect()
        # Optional data.
        self.data = data

    def draw(self, screen: pg.Surface):
        """Draws the widget on the given surface.
        Returns the area affected."""
        return screen.blit(self.image, self.rect)


class BaseScene:
    """The base class for a scene. Should not be instantiated."""

    # The scene to switch to next.
    next_scene = None

    # The arguments for the next scene, if applicable.
    kwargs = {}

    def __init__(self, screen_rect: pg.Rect):
        """Remember the screen_rect for future updates."""
        self.screen_rect = screen_rect

    def pump(self):
        """Pump network classes in the scene."""

    def events(self, events):
        """Handle pygame events."""

    def update_screen_size(self, screen_rect: pg.Rect):
        """Update scene based on new screen size."""
        self.screen_rect = screen_rect

    def update(self, dt):
        """Update everything in the scene."""

    def draw(self, screen):
        """Draw everything in the scene."""

    def quit(self):
        """Safely quit the scene."""


class StartScene(BaseScene):
    """The first scene the user sees.

    Gives the option to either host or join a server.
    """
    def __init__(self, screen_rect):
        super().__init__(screen_rect)
        # Create the widgets.
        self.host_button = Widget(DEFAULT_FONT.render("(H)ost Server", True, BLACK, GRAY))
        self.join_button = Widget(DEFAULT_FONT.render("(J)oin Server", True, BLACK, GRAY))
        self.quit_button = Widget(DEFAULT_FONT.render("(ESC) Quit", True, BLACK, GRAY))
        # Position the widgets on the screen.
        self.position_widgets()

    def position_widgets(self):
        """Place the widgets in their proper place on screen."""
        self.host_button.rect.centerx = self.screen_rect.centerx
        self.join_button.rect.centerx = self.screen_rect.centerx
        self.quit_button.rect.centerx = self.screen_rect.centerx
        self.host_button.rect.bottom = self.screen_rect.centery - self.join_button.rect.height
        self.join_button.rect.centery = self.screen_rect.centery
        self.quit_button.rect.top = self.screen_rect.centery + self.join_button.rect.height

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
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    # Check for button clicks.
                    if self.host_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.HOST
                    elif self.join_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.JOIN
                    elif self.quit_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.QUIT

    def draw(self, screen):
        self.host_button.draw(screen)
        self.join_button.draw(screen)
        self.quit_button.draw(screen)


class HostScene(BaseScene):
    """The server creation scene.

    Contains all the server config options.
    """
    def __init__(self, screen_rect):
        super().__init__(screen_rect)
        # Create the widgets.
        self.start_button = Widget(DEFAULT_FONT.render("(ENTER) Start Server", True, BLACK, GRAY))
        self.back_button = Widget(DEFAULT_FONT.render("(ESC) Main Menu", True, BLACK, GRAY))
        # Create the public checkbox.
        self.public = PUBLIC_SERVER
        self.public_button = Widget(DEFAULT_FONT.render(f"Public: {self.public}", True, BLACK, GRAY))
        # Create the player number box.
        self.number_of_players = 2  # The minimum number of players.
        self.number_box = Widget(DEFAULT_FONT.render(f"Players: {self.number_of_players}",
                                                     True, BLACK, GRAY))
        self.left_arrow = Widget(DEFAULT_FONT.render("< ", True, GRAY, BLACK))
        self.right_arrow = Widget(DEFAULT_FONT.render(" >", True, GRAY, BLACK))
        # Position the widgets on the screen.
        self.position_widgets()

    def position_widgets(self):
        """Place the widgets in their proper place on screen."""
        # Place the buttons.
        self.start_button.rect.centery = self.screen_rect.centery
        self.back_button.rect.centery = self.screen_rect.centery
        self.start_button.rect.x = self.screen_rect.centerx + 10
        self.back_button.rect.x = self.screen_rect.centerx - self.back_button.rect.width - 10
        # Place the number box.
        self.number_box.rect.centerx = self.screen_rect.centerx
        self.number_box.rect.bottom = self.start_button.rect.top - 20
        self.left_arrow.rect.centery = self.number_box.rect.centery
        self.right_arrow.rect.centery = self.number_box.rect.centery
        self.left_arrow.rect.right = self.number_box.rect.left
        self.right_arrow.rect.left = self.number_box.rect.right
        # Place the public checkbox.
        self.public_button.rect.centerx = self.screen_rect.centerx
        self.public_button.rect.bottom = self.number_box.rect.top - 20

    def update_public_button(self):
        """Update the public server setting."""
        self.public_button = Widget(DEFAULT_FONT.render(f"Public: {self.public}", True, BLACK, GRAY))
        self.public_button.rect.centerx = self.screen_rect.centerx
        self.public_button.rect.bottom = self.number_box.rect.top - 20

    def update_number_box(self):
        """Update the number box."""
        self.number_box = Widget(DEFAULT_FONT.render(f"Players: {self.number_of_players}",
                                                     True, BLACK, GRAY))
        # Place the number box.
        self.number_box.rect.centerx = self.screen_rect.centerx
        self.number_box.rect.bottom = self.start_button.rect.top - 20
        self.left_arrow.rect.centery = self.number_box.rect.centery
        self.right_arrow.rect.centery = self.number_box.rect.centery
        self.left_arrow.rect.right = self.number_box.rect.left
        self.right_arrow.rect.left = self.number_box.rect.right

    def update_screen_size(self, screen_rect):
        self.screen_rect = screen_rect
        self.position_widgets()

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_RETURN:
                    self.next_scene = NextScene.GAME
                    self.kwargs = {"server": True,
                                   "public": self.public,
                                   "players": self.number_of_players}
                elif event.key == pg.K_ESCAPE:
                    self.next_scene = NextScene.START
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    # Check for button clicks.
                    if self.start_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.GAME
                        self.kwargs = {"server": True,
                                       "public": self.public,
                                       "players": self.number_of_players}
                    elif self.back_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.START
                    elif self.public_button.rect.collidepoint(event.pos):
                        self.public = not self.public
                        self.update_public_button()
                    elif self.left_arrow.rect.collidepoint(event.pos):
                        self.number_of_players -= 1
                        if self.number_of_players > 1:
                            self.update_number_box()
                        else:
                            self.number_of_players += 1
                    elif self.right_arrow.rect.collidepoint(event.pos):
                        self.number_of_players += 1
                        if self.number_of_players < 9:
                            self.update_number_box()
                        else:
                            self.number_of_players -= 1

    def draw(self, screen):
        self.start_button.draw(screen)
        self.back_button.draw(screen)
        self.public_button.draw(screen)
        self.number_box.draw(screen)
        self.left_arrow.draw(screen)
        self.right_arrow.draw(screen)


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
        """Place the widgets in their proper place on screen."""
        # Place the buttons.
        self.start_button.rect.centery = self.screen_rect.centery
        self.back_button.rect.centery = self.screen_rect.centery
        self.start_button.rect.x = self.screen_rect.centerx + 10
        self.back_button.rect.x = self.screen_rect.centerx - self.back_button.rect.width - 10
        # Place the text box.
        self.text_box.rect.centerx = self.screen_rect.centerx
        self.text_box.rect.bottom = self.start_button.rect.top - 20

    def update_text_box(self):
        """Update the text box after text has been changed."""
        self.text_box = Widget(DEFAULT_FONT.render("Address: " + self.text, True, BLACK, GRAY))
        self.text_box.rect.centerx = self.screen_rect.centerx
        self.text_box.rect.bottom = self.start_button.rect.top - 20

    def update_screen_size(self, screen_rect):
        self.screen_rect = screen_rect
        self.position_widgets()

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                # Check for key commands.
                if event.key == pg.K_RETURN:
                    self.next_scene = NextScene.GAME
                    self.kwargs = {"join_address": self.text}
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
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    # Check for button clicks.
                    if self.start_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.GAME
                        self.kwargs = {"join_address": self.text}
                    elif self.back_button.rect.collidepoint(event.pos):
                        self.next_scene = NextScene.START

    def draw(self, screen):
        self.start_button.draw(screen)
        self.back_button.draw(screen)
        self.text_box.draw(screen)


class GameScene(BaseScene):
    """The game scene.

    Contains the game logic and network classes.
    """
    def __init__(self, screen_rect,
                 server: bool = False,
                 public: bool = PUBLIC_SERVER,
                 players: int = 2,
                 join_address: str = None):
        """Takes kwargs to configure the server and client for the game.

        server: bool = False; whether to create a server

        public: bool = False; whether the server is public with ngrok

        players: int = 0; the server won't start until this many players are online

        join_address: str = None; a string "host:port" to join the server
        """
        super().__init__(screen_rect)
        # Create the server.
        self.server = None
        if server:
            self.server = PieServer((DEFAULT_HOST, DEFAULT_PORT), players)
            # Make the server public.
            self.tunnel = None
            if public:
                if ngrok:
                    self.tunnel = ngrok.connect(DEFAULT_PORT, "tcp")
                    print("[Server] ngrok tunnel online: "
                          f"{self.tunnel.public_url} -> {self.server.get_address()}")
                else:
                    print("WARNING: Defaulting to private server.")
        # Create the client.
        if join_address is None:
            address = (DEFAULT_HOST, DEFAULT_PORT)
        else:
            address = join_address.rsplit(':')
            address = address[0], int(address[1])
        self.client = PieClient(self, address)

        # The scene variables.
        # Whether or not it is this player's turn.
        self.turn = False
        # The current card selected.
        self.card = None
        # The current scale of the cards.
        self.card_scale = CARD_SCALE

        # Create the widgets.
        text = "Not hosting"
        if self.server:
            if public:
                text = f"{self.tunnel.public_url.removeprefix('tcp://')}"
            else:
                text = f"{self.server.get_address()}"
        self.address_text = Widget(DEFAULT_FONT.render(f"Server: {text}", True, BLACK, GRAY))
        # Create the client status box.
        self.client_status = Widget(DEFAULT_FONT.render("No server", True, BLACK, GRAY))
        # How many cards the deck has.
        self.deck_status = Widget(DEFAULT_FONT.render("Deck: No cards", True, BLACK, GRAY))
        # The player button list.
        self.player_buttons = []
        # The card list.
        self.card_widgets = []

        # Position the widgets.
        self.position_widgets()

    def position_widgets(self):
        """Place the widgets in their proper place on screen."""
        self.address_text.rect.midtop = self.screen_rect.midtop
        self.client_status.rect.midtop = self.address_text.rect.midbottom
        self.deck_status.rect.midtop = self.client_status.rect.midbottom

    def update_client_status(self, status):
        """Called from the PieClient on certain Network events.
        Updates the client status bar."""
        self.client_status = Widget(DEFAULT_FONT.render(status, True, BLACK, GRAY))
        self.client_status.rect.midtop = self.address_text.rect.midbottom

    def update_deck_status(self, status):
        """Called from the PieClient on certain Network events.
        Updates the deck status bar."""
        self.deck_status = Widget(DEFAULT_FONT.render(status, True, BLACK, GRAY))
        self.deck_status.rect.midtop = self.client_status.rect.midbottom

    def update_stats(self, stats):
        """Called from the PieClient on certain Network events.
        Updates the player buttons on the screen."""
        # Clear the current stats.
        self.player_buttons = []
        # Create the new stats.
        for player_id, stat in enumerate(stats):
            w = Widget(make_player_button(player_id, stat[0], stat[1], self.client.player_id), player_id)
            w.rect.top = self.deck_status.rect.bottom + 20
            if len(self.player_buttons):
                w.rect.left = self.player_buttons[-1].rect.right + 10
            else:
                w.rect.left = 10
            self.player_buttons.append(w)

    def update_cards(self, cards):
        """Called from the PieClient on certain Network events.
        Given a list of ranks, updates the player's hand.
        There must be at least one player button or this method will crash."""
        # Clear the current hand.
        self.card_widgets = []
        # Create the new card widgets.
        for index, card in enumerate(cards):
            w = Widget(self.scale_card(card_images[ranks_to_pie[card]]), card)
            w.rect.top = self.player_buttons[0].rect.bottom + 20
            w.rect.left = index * w.rect.centerx
            self.card_widgets.append(w)

    def scale_card(self, image: pg.Surface) -> pg.Surface:
        """Scales a given card surface by self.card_scale."""
        w, h = int(image.get_width() * self.card_scale), int(image.get_height() * self.card_scale)
        return pg.transform.scale(image, (w, h))

    def update_turn(self):
        # It is now this player's turn.
        self.turn = True
        self.card = None

    def update_screen_size(self, screen_rect):
        self.screen_rect = screen_rect
        self.position_widgets()

    def pump(self):
        if self.server:
            self.server.pump()
        self.client.pump()

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.next_scene = NextScene.START
                    self.quit()
                elif event.key == pg.K_UP:
                    self.card_scale += 0.01
                    self.card_scale = min(self.card_scale, 0.2)
                    if self.card_widgets:
                        self.update_cards([card.data for card in self.card_widgets])
                elif event.key == pg.K_DOWN:
                    self.card_scale -= 0.01
                    self.card_scale = max(self.card_scale, 0.02)
                    if self.card_widgets:
                        self.update_cards([card.data for card in self.card_widgets])
            elif event.type == pg.MOUSEBUTTONUP:
                # Only allow clicking buttons if it is your turn.
                if self.turn:
                    # Get the card selected.
                    for card in self.card_widgets:
                        if card.rect.collidepoint(event.pos):
                            self.card = card.data
                            text = ranks_to_pie[self.card].removesuffix(".png")
                            self.update_client_status(f"Your turn: {text} selected")
                            continue
                    # Get the player asked.
                    for player in self.player_buttons:
                        if player.rect.collidepoint(event.pos):
                            # Don't ask yourself for a card.
                            if self.player_buttons.index(player) == self.client.player_id:
                                continue
                            # Only send data if a card has been picked.
                            if self.card is not None:
                                self.client.Send({"action": "ask",
                                                  "player": player.data,
                                                  "rank": self.card})
                                # Reset the turn.
                                self.turn = False
                                self.card = None
                                self.update_client_status("Not your turn")
                            continue

    def draw(self, screen):
        # Display the exit control right below the FPS.
        screen.blit(DEFAULT_FONT.render("ESC to quit.",
                                        True, BLACK), (0, DEFAULT_FONT.get_height()))
        # Display the card scale controls at top right.
        screen.blit(DEFAULT_FONT.render("UP/DOWN to scale cards.", True, BLACK),
                    (self.screen_rect.right - DEFAULT_FONT.size("UP/DOWN to scale cards.")[0], 0))

        # Display widgets.
        self.address_text.draw(screen)
        self.client_status.draw(screen)
        self.deck_status.draw(screen)
        for button in self.player_buttons:
            button.draw(screen)
        for card in self.card_widgets:
            rect = card.draw(screen)
            # Draw a highlight for selected ranks.
            if self.card == card.data:
                pg.draw.rect(screen, CYAN, rect, 2)

    def quit(self):
        # Quit the client.
        self.client.quit()
        # Quit the server.
        if self.server:
            self.server.quit()
            # Take the tunnel offline.
            if self.tunnel:
                ngrok.disconnect(self.tunnel.public_url)
                print("[Server] ngrok tunnel offline.")
