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
            ray_casting_result (List[Tuple[float, float, int, float]]): List to store ray casting results
            objects_to_render (List[Tuple[float, pg.Surface, Tuple[int, int]]]): List to store objects to render
            textures (List[pg.Surface]): List of wall textures
        """
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self) -> None:
        """
        Get the objects to render based on ray casting results.
        """
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # Skip empty results (no wall found)
            if texture is None or depth == float("inf"):
                continue

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE,
                    texture_height,
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # Apply fog effect
            if depth > FOG_START:
                fog_factor = min(1.0, (depth - FOG_START) / (FOG_END - FOG_START))
                fog_surface = pg.Surface(wall_column.get_size(), pg.SRCALPHA)
                fog_surface.fill(
                    (0, 0, 0, int(255 * fog_factor))
                )  # Black fog with alpha
                wall_column.blit(fog_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self) -> None:
        """
        Perform raycasting calculations for the current frame.

        This method casts rays from the player's position to determine wall distances
        and positions. It handles both horizontal and vertical wall intersections,
        calculating the shortest distance to walls for proper 3D rendering.
        """
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
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

            found_hor_wall = False
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)

                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    found_hor_wall = True
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            if not found_hor_wall:
                depth_hor = float("inf")
                texture_hor = None  # Reset texture if no wall found

            # Verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            found_vert_wall = False
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)

                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    found_vert_wall = True
                    break

                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if not found_vert_wall:
                depth_vert = float("inf")
                texture_vert = None  # Reset texture if no wall found

            # Depth and texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # Skip if no wall was found or if texture is None
            if depth == float("inf") or texture is None:
                # Add empty result to maintain view proportion
                self.ray_casting_result.append((float("inf"), 0, None, 0))
                ray_angle += DELTA_ANGLE
                continue

            # Remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Raycasting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self) -> None:
        """
        Update the raycasting calculations for the current frame.
        """
        self.ray_cast()
        self.get_objects_to_render()
