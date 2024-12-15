"""
Map Module

This module defines the game map layout and provides functionality for
map initialization, rendering, and collision detection.
"""

from typing import TYPE_CHECKING, Dict, List, Tuple

import pygame as pg

if TYPE_CHECKING:
    from main import Game

# Map layout where 1 represents walls and _ (False) represents empty spaces
_ = False
mini_map: List[List[int]] = [
    # Entry Section (Computer Lab)
    [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, 9, 9, _, _, _, _, _, _, _, _, 10, 10, _, 15],
    [15, _, 9, _, _, _, _, _, _, _, _, _, _, 10, _, 15],
    [15, _, _, _, _, 11, 11, _, _, 11, 11, _, _, _, _, 15],
    [15, _, _, _, _, 11, 11, _, _, 11, 11, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, 17, 17, _, _, _, _, _, _, _, _, _, _, 17, 17, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    # Tech Hub
    [15, _, _, _, _, 1, 1, _, _, 1, 1, _, _, _, _, 15],
    [15, _, _, _, _, 1, _, _, _, _, 1, _, _, _, _, 15],
    [15, _, 2, 2, _, _, _, _, _, _, _, _, 2, 2, _, 15],
    [15, _, 2, 2, _, _, _, _, _, _, _, _, 2, 2, _, 15],
    [15, _, _, _, _, _, 3, 3, 3, 3, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, 18, 18, _, _, _, _, _, _, _, _, _, _, 18, 18, 15],
    # Ship Corridors Start
    [15, _, _, _, _, _, 17, _, _, 17, _, _, _, _, _, 15],
    [15, _, _, _, _, _, 17, _, _, 17, _, _, _, _, _, 15],
    [15, _, _, 19, 19, 19, 19, _, _, 19, 19, 19, 19, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, 19, 19, _, _, _, _, _, _, _, _, _, _, 19, 19, 15],
    [15, _, _, _, _, _, 19, _, _, 19, _, _, _, _, _, 15],
    [15, _, _, _, _, _, 19, _, _, 19, _, _, _, _, _, 15],
    # Ventilation Maze Start
    [15, _, _, 16, 16, 16, 16, _, _, 16, 16, 16, 16, _, _, 15],
    [15, _, _, 16, _, _, _, _, _, _, _, _, 16, _, _, 15],
    [15, _, _, 16, _, _, _, _, _, _, _, _, 16, _, _, 15],
    [15, _, _, 16, _, _, 16, 16, 16, 16, _, _, 16, _, _, 15],
    [15, _, _, _, _, _, 16, _, _, 16, _, _, _, _, _, 15],
    [15, _, _, _, _, _, 16, _, _, 16, _, _, _, _, _, 15],
    [15, _, _, 16, _, _, 16, _, _, 16, _, _, 16, _, _, 15],
    [15, _, _, 16, _, _, _, _, _, _, _, _, 16, _, _, 15],
    # Industrial Zone Start
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, 4, 4, _, _, _, _, _, _, _, _, 5, 5, _, 15],
    [15, _, 4, _, _, _, _, _, _, _, _, _, _, 5, _, 15],
    [15, _, _, _, _, 6, 6, _, _, 6, 6, _, _, _, _, 15],
    [15, _, _, _, _, 6, _, _, _, _, 6, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, 7, 7, _, _, _, _, _, _, _, _, _, _, 7, 7, 15],
    [15, _, _, _, _, _, 8, _, _, 8, _, _, _, _, _, 15],
    # Final Section Start
    [15, _, _, _, _, _, 8, _, _, 8, _, _, _, _, _, 15],
    [15, _, _, 12, 12, 12, 12, _, _, 12, 12, 12, 12, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, 13, 13, _, _, _, _, _, _, _, _, 13, 13, _, 15],
    [15, _, 13, _, _, _, _, _, _, _, _, _, _, 13, _, 15],
    [15, _, _, _, _, 14, 14, _, _, 14, 14, _, _, _, _, 15],
    [15, _, _, _, _, 14, _, _, _, _, 14, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    # Boss Arena
    [15, 13, 13, _, _, _, _, _, _, _, _, _, _, 13, 13, 15],
    [15, _, _, _, _, _, 16, _, _, 16, _, _, _, _, _, 15],
    [15, _, _, _, _, _, 16, _, _, 16, _, _, _, _, _, 15],
    [15, _, _, 19, 19, 19, 19, _, _, 19, 19, 19, 19, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    # Final Rooms
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 15],
    [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
]


class Map:
    """
    Map class handling the game world's layout and rendering.

    This class manages the game map, including wall positions and their rendering.
    It converts the 2D array representation into a dictionary of wall positions
    for efficient collision detection.

    Attributes:
        game (str): Reference to the main game instance
        mini_map (List[List[int]]): 2D array representing the map layout
        world_map (Dict[Tuple[int, int], int]): Dictionary of wall positions for collision detection
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize a new map instance.

        Args:
            game (Game): Reference to the main game instance
        """
        self.game = game
        self.mini_map = mini_map
        self.world_map: Dict[Tuple[int, int], int] = {}
        self.get_map()

    def get_map(self) -> None:
        """
        Convert the 2D array map representation into a dictionary of wall positions.

        Iterates through the mini_map and creates a dictionary where keys are (x, y)
        coordinates and values are the wall type (1 for standard walls).
        """
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self) -> None:
        """
        Render the map walls on the screen.

        Draws rectangles for each wall position in the world_map using
        the game's display surface.
        """
        [
            pg.draw.rect(
                self.game.screen, "darkgrey", (pos[0] * 100, pos[1] * 100, 100, 100), 2
            )
            for pos in self.world_map
        ]
