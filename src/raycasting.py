import math
from typing import TYPE_CHECKING

import pygame as pg

from settings import *

if TYPE_CHECKING:
    from main import Game


class RayCasting:
    """
    Handles the raycasting calculations for rendering the 3D view.

    This class implements the raycasting algorithm that creates the 3D perspective
    by casting rays from the player's position and calculating wall distances.

    Attributes:
        game (Game): Reference to the main game instance
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize the RayCasting instance.

        Args:
            game (Game): Reference to the main game instance
        """
        self.game = game

    def ray_cast(self) -> None:
        """
        Perform raycasting calculations for the current frame.

        This method casts rays from the player's position to determine wall distances
        and positions. It handles both horizontal and vertical wall intersections,
        calculating the shortest distance to walls for proper 3D rendering.
        """
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)

                if tile_hor in self.game.map.world_map:
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)

                if tile_vert in self.game.map.world_map:
                    break

                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Depth
            depth = depth_vert if depth_vert < depth_hor else depth_hor

            # Draw for debug
            pg.draw.line(
                self.game.screen,
                "yellow",
                (100 * ox, 100 * oy),
                (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a),
                2,
            )

            ray_angle += DELTA_ANGLE

    def update(self) -> None:
        """
        Update the raycasting calculations for the current frame.
        """
        self.ray_cast()
