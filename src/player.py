"""
Player Module

This module implements the player character functionality including movement,
collision detection, and rendering for the Doom-style raycasting game.
"""

import math
from typing import Any, Tuple

import pygame as pg

from settings import *


class Player:
    """
    Player class handling all player-related functionality.

    This class manages the player's position, movement, rotation, collision detection,
    and rendering in the game world.

    Attributes:
        game (Any): Reference to the main game instance
        x (float): Player's x position in the game world
        y (float): Player's y position in the game world
        angle (float): Player's viewing angle in radians
    """

    def __init__(self, game: Any) -> None:
        """
        Initialize a new player instance.

        Args:
            game (Any): Reference to the main game instance
        """
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self) -> None:
        """
        Handle player movement based on keyboard input.

        Updates player position and rotation based on WASD keys for movement
        and arrow keys for rotation. Applies collision detection and normalizes
        the viewing angle.
        """
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()

        # Handle WASD movement
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        # Handle rotation with arrow keys
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED

        self.angle %= math.tau

    def check_wall(self, x: int, y: int) -> bool:
        """
        Check if a given position contains a wall.

        Args:
            x (int): X coordinate to check
            y (int): Y coordinate to check

        Returns:
            bool: True if position is empty, False if contains a wall
        """
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx: float, dy: float) -> None:
        """
        Check and handle collision with walls when moving.

        Args:
            dx (float): Attempted movement in x direction
            dy (float): Attempted movement in y direction
        """
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx

        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self) -> None:
        """
        Render the player's position and viewing direction on the screen.
        """
        pg.draw.line(
            self.game.screen,
            "yellow",
            (self.x * 100, self.y * 100),
            (
                self.x * 100 + WIDTH * math.cos(self.angle),
                self.y * 100 + WIDTH * math.sin(self.angle),
            ),
            2,
        )

        pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    def update(self) -> None:
        """
        Update the player's state by handling movement.
        """
        self.movement()

    @property
    def pos(self) -> Tuple[float, float]:
        """
        Get the player's current position.

        Returns:
            Tuple[float, float]: (x, y) coordinates of the player's position
        """
        return self.x, self.y

    @property
    def map_pos(self) -> Tuple[int, int]:
        """
        Get the player's current position on the map.

        Returns:
            Tuple[int, int]: (x, y) coordinates of the player's position on the map
        """
        return int(self.x), int(self.y)
