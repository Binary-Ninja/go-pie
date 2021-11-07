#!/usr/bin/env python3
"""The main file to run for online Go Pie."""

# Standard library imports.
import sys

# Third party library imports.
import pygame as pg

# Local library imports.
from config import *
from assets import *
from scenes import *


class Main:
    """The main application for Go Pie."""
    def __init__(self):
        # Create the display.
        self.screen = pg.display.set_mode(DEFAULT_SCREEN_SIZE, pg.RESIZABLE)
        # Get the display Rect.
        self.screen_rect = self.screen.get_rect()
        # Set the screen caption.
        pg.display.set_caption("Go Pie")
        # The clock to keep track of dt and fps.
        self.clock = pg.time.Clock()
        # The time that passed between the last two frames in milliseconds.
        self.dt = 0

        # Keep track of the current scene.
        self.scene = StartScene(self.screen_rect)

    def terminate(self):
        """Close the window and end the process."""
        pg.quit()
        sys.exit()

    def pump(self):
        """Tick the clock and pump network classes."""
        # Tick clock once per game loop for dt and fps.
        self.dt = self.clock.tick()
        # Switch scenes.
        if scene := self.scene.next_scene:
            if scene == NextScene.QUIT:
                self.terminate()
            elif scene == NextScene.START:
                self.scene = StartScene(self.screen_rect)
            elif scene == NextScene.HOST:
                self.scene = HostScene(self.screen_rect)
            elif scene == NextScene.JOIN:
                self.scene = JoinScene(self.screen_rect)
        # Pump the network classes in the current scene.
        self.scene.pump()

    def events(self):
        """Handle pygame events."""
        # Get the events from pygame event handler.
        events = pg.event.get()
        # Handle top level events.
        for event in events:
            if event.type == pg.QUIT:
                # The window has been closed.
                self.terminate()
            elif event.type == pg.VIDEORESIZE:
                # The window has been resized.
                self.screen = pg.display.set_mode(event.size, pg.RESIZABLE)
                # Get the display Rect.
                self.screen_rect = self.screen.get_rect()
                # Tell the current scene the display has changed.
                self.scene.update_screen_size(self.screen_rect)
        # Delegate events to current scene.
        self.scene.events(events)

    def update(self):
        """Update everything before drawing."""
        # Update the current scene.
        self.scene.update(self.dt)

    def render_text(self, text):
        """Return rendered anti aliased text surface."""
        return DEFAULT_FONT.render(text, True, BLACK, WHITE)

    def draw(self):
        """Draw everything to the screen."""
        # Draw the background.
        self.screen.fill(WHITE)

        # Draw the current scene.
        self.scene.draw(self.screen)

        # Display the FPS.
        text_surf = self.render_text(f"FPS: {self.clock.get_fps():.0F}")
        self.screen.blit(text_surf, (0, 0))

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
    # Initialize pygame.
    pg.init()
    # Create and run the main application.
    m = Main()
    m.run()


if __name__ == "__main__":
    main()
