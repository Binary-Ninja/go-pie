#!/usr/bin/env python3
"""The main file to run for online Go Pie."""

# Standard library imports.
import sys
import json
from pathlib import Path

# Third-party library imports.
import pygame as pg

# Import ngrok if available.
try:
    from pyngrok import ngrok
except ImportError:
    print("WARNING: ngrok not found. Public server creation unavailable.")
    ngrok = None

# Local library imports.
from server import PieServer
from client import PieClient


# Try to load in the config file.
try:
    # Decode json configuration file.
    with open(Path() / "config.json", "r") as file:
        config_data = json.load(file)
except FileNotFoundError:
    # The file doesn't exist, so create an empty configuration.
    config_data = {}

# Extract configuration data with default values.
# The starting screen resolution.
DEFAULT_SIZE = config_data.get("screen_resolution", (800, 600))
# The default port to host servers on.
DEFAULT_PORT = config_data.get("default_port", 5071)
# Whether the server is public with ngrok or not.
PUBLIC_SERVER = config_data.get("public_server", False)
# The address of the server for clients to join.
SERVER_ADDRESS = config_data.get("server_address", f"localhost:{DEFAULT_PORT}").split(":")
SERVER_ADDRESS = SERVER_ADDRESS[0], int(SERVER_ADDRESS[1])  # Create a tuple of (host, port).


class Main:
    """The main application for Go Pie."""
    def __init__(self):
        # Initialize pygame.
        pg.init()
        # Create the display.
        self.screen = pg.display.set_mode(DEFAULT_SIZE, pg.RESIZABLE)
        # Set the screen caption.
        pg.display.set_caption("Go Pie")
        # The clock to keep track of dt and fps.
        self.clock = pg.time.Clock()
        # The time that passed between the last two frames in milliseconds.
        self.dt = 0

        # The font to draw text to the screen.
        self.font = pg.font.Font(None, 22)

        # The server and client of this application.
        self.client = None
        self.server = None
        # The public network tunnel.
        self.tunnel = None

    def pump(self):
        """Tick the clock and pump network classes."""
        # Tick clock once per game loop for dt and fps.
        self.dt = self.clock.tick()
        # Pump network classes once per game loop.
        if self.client:
            self.client.pump()
        if self.server:
            self.server.pump()

    def events(self):
        """Handle the pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # The window has been closed.
                pg.quit()
                sys.exit()
            elif event.type == pg.VIDEORESIZE:
                # The window has been resized.
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_h:
                    # Create and join localhost server if no client is running.
                    if self.client is None:
                        self.server = PieServer(localaddr=("localhost", DEFAULT_PORT))
                        self.client = PieClient(self.server.address)
                        # Make the server public.
                        if PUBLIC_SERVER:
                            if ngrok is not None:
                                # Create the network tunnel.
                                self.tunnel = ngrok.connect(DEFAULT_PORT, "tcp")
                                print("[Server] ngrok tunnel online: "
                                      f"{self.tunnel.public_url} -> {self.tunnel.config['addr']}")
                            else:
                                # ngrok is not available.
                                print("[Server] Public server creation unavailable. "
                                      "Defaulting to localhost.")

                elif event.key == pg.K_j:
                    # Join the server as specified in config if no client is running.
                    if self.client is None:
                        self.client = PieClient(SERVER_ADDRESS)

                elif event.key == pg.K_q:
                    # Quit the server and client, if running.
                    if self.client:
                        self.client.quit()
                        self.client = None
                    if self.server:
                        self.server.quit()
                        self.server = None
                        # Take network tunnel offline.
                        if self.tunnel is not None:
                            ngrok.disconnect(self.tunnel.public_url)
                            self.tunnel = None

    def update(self):
        """Update everything before drawing."""

    def render_text(self, text):
        """Return rendered anti aliased text surface."""
        return self.font.render(text, True, (101, 123, 131), (253, 246, 227))

    def draw(self):
        """Draw everything to the screen."""
        # Clear the screen.
        self.screen.fill((253, 246, 227))
        # Display the FPS.
        text_surf = self.render_text(f"FPS: {self.clock.get_fps():.0F}")
        self.screen.blit(text_surf, (0, 0))

        # Display the server address.
        if self.server:
            # Display public address if online, local address otherwise.
            if self.tunnel is not None:
                server_text = f"Server IP: {self.tunnel.public_url.removeprefix('tcp://')}"
            else:
                server_text = f"Server IP: {self.server.get_address()}"
            text_surf = self.render_text(server_text)
            self.screen.blit(text_surf, (0, 20))
        # Display the client address.
        if self.client:
            text_surf = self.render_text(f"Client IP: {self.client.get_address()}")
            self.screen.blit(text_surf, (0, 40))

        # Flip the display.
        pg.display.flip()

    def run(self):
        """The main loop of the application."""
        while True:
            self.pump()
            self.events()
            self.update()
            self.draw()


def main():
    # Create and run the main application.
    m = Main()
    m.run()


if __name__ == "__main__":
    main()
