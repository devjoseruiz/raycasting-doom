#!/usr/bin/env python3
"""
Doom-style minigame using raycasting technique and Pygame

This module implements a basic Doom-style raycasting game using Pygame.
It handles the main game loop, initialization, and core game mechanics.
"""

import sys
import pygame as pg
from typing import Any

from map import Map
from player import Player
from settings import *


class Game:
    """
    Main game class that handles initialization, game loop, and core game mechanics.

    This class is responsible for setting up the game window, managing the game loop,
    handling events, and coordinating between different game components like the map
    and player.

    Attributes:
        screen (pg.Surface): The main game display surface
        clock (pg.time.Clock): Game clock for controlling FPS
        delta_time (float): Time elapsed between frames
        map (Map): Game map instance
        player (Player): Player instance
    """

    def __init__(self) -> None:
        """Initialize the game, set up display and create a new game instance."""
        pg.init()
        self.screen: pg.Surface = pg.display.set_mode(RES)
        self.clock: pg.time.Clock = pg.time.Clock()
        self.delta_time: float = 1
        self.new_game()

    def new_game(self) -> None:
        """Create a new game state with fresh map and player instances."""
        self.map = Map(self)
        self.player = Player(self)

    def update(self) -> None:
        """
        Update game state for the current frame.
        
        Updates player position, refreshes display, and manages frame timing.
        """
        self.player.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self) -> None:
        """
        Render the current game state.
        
        Clears the screen and draws the map and player.
        """
        self.screen.fill("black")
        self.map.draw()
        self.player.draw()

    def check_events(self) -> None:
        """
        Handle game events including quit conditions.
        
        Processes pygame events and handles game exit conditions (ESC key or window close).
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()

    def run(self) -> None:
        """
        Main game loop.
        
        Continuously runs the game by checking events, updating game state,
        and drawing to the screen.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
