#!/usr/bin/env python3
"""The main file to run for online Go Pie."""

import sys

import pygame as pg

DEFAULT_SIZE = 800, 600


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

    def events(self):
        """Handle the pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # The window has been closed.
                pg.quit()
                sys.exit()

    def update(self):
        """Update everything before drawing."""

    def draw(self):
        """Draw everything to the screen."""
        # Clear the screen.
        self.screen.fill((253, 246, 227))
        # Flip the display.
        pg.display.flip()

    def run(self):
        """The main loop of the application."""
        while True:
            self.events()
            self.update()
            self.draw()


def main():
    # Create and run the main application.
    m = Main()
    m.run()


if __name__ == "__main__":
    main()
