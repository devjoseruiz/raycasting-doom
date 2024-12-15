import math
from typing import TYPE_CHECKING

import pygame as pg

from settings import *

if TYPE_CHECKING:
    from main import Game


class ObjectRenderer:
    """
    Handles the rendering of all game objects, including walls, skybox, and floor.

    This class is responsible for loading textures, managing the skybox offset,
    and rendering all visual elements of the game in the correct order.

    Attributes:
        game (Game): Reference to the main game instance
        screen (pygame.Surface): The game's display surface
        wall_textures (dict): Dictionary of loaded wall textures
        skybox (pygame.Surface): The skybox texture
        skybox_offset (float): Current horizontal offset of the skybox
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize the ObjectRenderer instance.

        Args:
            game (Game): Reference to the main game instance
        """
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.skybox = self.get_texture("skybox.png", (WIDTH, HEIGHT))
        self.skybox_offset = 0

    def draw(self) -> None:
        """
        Main drawing method that renders all game objects.

        Renders the game elements in the correct order:
        1. Background (skybox and floor)
        2. Game objects (walls)
        """
        self.draw_background()
        self.render_game_objects()

    def draw_background(self) -> None:
        """
        Draws the background elements (skybox and floor).

        The skybox is rendered with a parallax effect based on player rotation,
        and the floor is drawn as a solid color rectangle in the bottom half of the screen.
        """
        rotation_factor = self.game.player.angle / (2 * math.pi)
        self.skybox_offset = (rotation_factor * WIDTH * 4) % WIDTH

        self.screen.blit(self.skybox, (-self.skybox_offset, 0))
        self.screen.blit(self.skybox, (-self.skybox_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self) -> None:
        """
        Renders all game objects (walls) based on raycasting results.

        Objects are rendered in order from furthest to nearest to create
        proper depth perception.
        """
        list_objects = sorted(
            self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True
        )
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def load_wall_textures(self) -> dict[int, pg.Surface]:
        """
        Loads all wall textures from the resources directory.

        Returns:
            dict: Dictionary of loaded and scaled wall textures
        """
        return {
            1: self.get_texture("walls/brickface.png"),
            2: self.get_texture("walls/brickquartz.png"),
            3: self.get_texture("walls/brickruined.png"),
            4: self.get_texture("walls/brickstone.png"),
            5: self.get_texture("walls/comp.png"),
            6: self.get_texture("walls/comp1.png"),
            7: self.get_texture("walls/comp2.png"),
            8: self.get_texture("walls/dirtbrown.png"),
            9: self.get_texture("walls/dirtgray.png"),
            10: self.get_texture("walls/dirtred.png"),
            11: self.get_texture("walls/shipgratewall.png"),
            12: self.get_texture("walls/shipventskin.png"),
            13: self.get_texture("walls/shipwall.png"),
            14: self.get_texture("walls/shipwall1.png"),
            15: self.get_texture("walls/shipwall2.png"),
            16: self.get_texture("walls/shipwall3.png"),
            17: self.get_texture("walls/shipwall4.png"),
            18: self.get_texture("walls/shipwall5.png"),
            19: self.get_texture("walls/shipwall6.png"),
        }

    @staticmethod
    def get_texture(
        path: str, res: tuple[int, int] = (TEXTURE_SIZE, TEXTURE_SIZE)
    ) -> pg.Surface:
        """
        Loads and scales a texture from the resources directory.

        Args:
            path (str): Path to the texture file relative to the textures folder
            res (Tuple[int, int], optional): Resolution to scale the texture to.
                Defaults to (TEXTURE_SIZE, TEXTURE_SIZE).

        Returns:
            pygame.Surface: The loaded and scaled texture
        """
        texture = pg.image.load(str(TEXTURES_FOLDER / path)).convert_alpha()
        return pg.transform.scale(texture, res)
