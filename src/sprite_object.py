"""
Sprite Object Module

This module implements sprite rendering and animation functionality for the game.
It handles both static and animated sprites, including their projection, scaling,
and positioning in the world.
"""

import math
import os
from collections import deque
from typing import TYPE_CHECKING, Deque, Tuple

import pygame as pg

from settings import *

if TYPE_CHECKING:
    from main import Game


class SpriteObject:
    """
    Base class for handling static sprites in the game world.

    This class manages sprite loading, positioning, and projection calculations
    for rendering sprites in the environment.

    Attributes:
        game (Game): Reference to the main game instance
        player: Reference to the player instance
        x (float): X position in the game world
        y (float): Y position in the game world
        image (pg.Surface): Sprite texture
        IMAGE_WIDTH (int): Width of the sprite texture
        IMAGE_HALF_WIDTH (int): Half width of the sprite texture
        IMAGE_RATIO (float): Width to height ratio of the sprite
        dx (float): Distance from player to sprite in x-axis
        dy (float): Distance from player to sprite in y-axis
        theta (float): Angle between player and sprite
        screen_x (float): X position on screen where sprite should be rendered
        dist (float): Euclidean distance from player to sprite
        norm_dist (float): Distance used for projection (adjusted for fisheye)
        sprite_half_width (float): Half width of the projected sprite
        SPRITE_SCALE (float): Scale factor for the sprite
        SPRITE_HEIGHT_SHIFT (float): Vertical position adjustment
    """

    def __init__(
        self,
        game: "Game",
        path: str,
        pos: Tuple[float, float],
        scale: float,
        shift: float,
    ):
        """
        Initialize a sprite object.

        Args:
            game (Game): Reference to the main game instance
            path (str): Path to the sprite texture file
            pos (Tuple[float, float]): Initial position (x, y) in the game world
            scale (float): Scale factor for the sprite
            shift (float): Vertical position adjustment
        """
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        (
            self.dx,
            self.dy,
            self.theta,
            self.screen_x,
            self.dist,
            self.norm_dist,
            self.sprite_half_width,
        ) = (0, 0, 0, 0, 1, 1, 0)
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self) -> None:
        """
        Calculate and prepare the sprite projection for rendering.

        Computes the sprite's size and position on screen based on its distance
        from the player and adds it to the rendering queue.
        """
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = (
            self.screen_x - self.sprite_half_width,
            HALF_HEIGHT - proj_height // 2 + height_shift,
        )

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self) -> None:
        """
        Update sprite position relative to the player.

        Calculates distances, angles, and screen position of the sprite,
        then triggers projection if the sprite is visible.
        """
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle

        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)

        if (
            -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH)
            and self.norm_dist > 1.0
        ):
            self.get_sprite_projection()

    def update(self) -> None:
        """Update the sprite's state and prepare it for rendering."""
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    """
    Class for handling animated sprites in the game world.

    Extends SpriteObject to add animation capabilities by cycling through
    a sequence of sprite frames.

    Attributes:
        animation_time (int): Time in milliseconds between animation frames
        path (str): Directory path containing animation frames
        images (Deque[pg.Surface]): Collection of animation frame images
        animation_time_prev (int): Timestamp of last animation update
        animation_trigger (bool): Flag indicating if animation should update
    """

    def __init__(
        self,
        game: "Game",
        path: str,
        pos: Tuple[float, float],
        scale: float,
        shift: float,
        animation_time: int = 120,
    ):
        """
        Initialize an animated sprite.

        Args:
            game (Game): Reference to the main game instance
            path (str): Path to the directory containing animation frames
            pos (Tuple[float, float]): Initial position (x, y) in the game world
            scale (float): Scale factor for the sprite
            shift (float): Vertical position adjustment
            animation_time (int): Time in milliseconds between animation frames
        """
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = os.path.dirname(path)
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self) -> None:
        """
        Update the animated sprite's state.

        Updates both the sprite's position and its animation state.
        """
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images: Deque[pg.Surface]) -> None:
        """
        Advance the animation to the next frame if triggered.

        Args:
            images (Deque[pg.Surface]): Collection of animation frame images
        """
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self) -> None:
        """
        Check if it's time to advance to the next animation frame.

        Updates animation_trigger based on the elapsed time since the last frame.
        """
        self.animation_trigger = False
        time_now = pg.time.get_ticks()

        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path: str) -> Deque[pg.Surface]:
        """
        Load all animation frames from the specified directory.

        Args:
            path (str): Path to directory containing animation frames

        Returns:
            Deque[pg.Surface]: Collection of loaded animation frame images
        """
        images = deque()

        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(os.path.join(path, file_name)).convert_alpha()
                images.append(img)

        return images
