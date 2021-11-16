#!/usr/bin/env python3
"""The main file to run for online Go Pie."""

# Standard library imports.
import sys
import random

# Third party library imports.
import pygame as pg

# Local library imports.
from config import *
from assets import *
from scenes import NextScene, StartScene, HostScene, JoinScene, GameScene, Particle


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

        # Convert the card images.
        for card_rank, card_image in card_images.items():
            card_images[card_rank] = card_image.convert()

        # Keep track of the current scene.
        self.scene = StartScene(self.screen_rect)
        # Store the background particles.
        self.particles = pg.sprite.Group()
        # Create some particles.
        for _ in range(10):
            self.create_new_particle(bottom=False)

    def create_new_particle(self, bottom=True):
        if bottom:
            bottom = self.screen_rect.bottom + 100
        else:
            bottom = random.randint(0, self.screen_rect.bottom)
        pos = random.randint(0, self.screen_rect.right), bottom
        size = (random.randint(50, 200),) * 2
        angle = random.randint(0, 359)
        pos_vel = (0, -random.randint(50, 100))
        angle_vel = random.randint(45, 180)
        if random.random() > 0.5:
            angle_vel *= -1
        self.particles.add(Particle(pos, size, angle, pos_vel, angle_vel))

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
            elif scene == NextScene.GAME:
                self.scene = GameScene(self.screen_rect, **self.scene.kwargs)
        # Pump the network classes in the current scene.
        self.scene.pump()

    def events(self):
        """Handle pygame events."""
        # Get the events from pygame event handler.
        events = pg.event.get()
        # Handle top level events.
        for event in events:
            if event.type == pg.QUIT:
                # Safely quit the current scene.
                self.scene.quit()
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
        # Update the particles.
        for particle in self.particles:
            particle.update(self.dt)
            # Kill particles off screen.
            if particle.rect.bottom < 0:
                particle.kill()
        # Add new particles.
        while len(self.particles) < 10:
            self.create_new_particle()

        # Update the current scene.
        self.scene.update(self.dt)

    def render_text(self, text):
        """Return rendered anti aliased text surface."""
        return DEFAULT_FONT.render(text, True, BLACK)

    def draw(self):
        """Draw everything to the screen."""
        # Draw the background.
        self.screen.fill(TAN)

        # Draw the background particles.
        self.particles.draw(self.screen)

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
