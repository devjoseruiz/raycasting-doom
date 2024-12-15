"""
Object Handler Module

This module manages the creation, storage, and updating of all sprite objects in the game.
It handles both static and animated sprites, organizing them in a centralized location
for easier management and batch updates.
"""

from typing import TYPE_CHECKING, List, Union

from settings import *
from sprite_object import AnimatedSprite, SpriteObject

if TYPE_CHECKING:
    from pathlib import Path

    from main import Game


class ObjectHandler:
    """
    Class responsible for managing all sprite objects in the game.

    This class serves as a central manager for all sprite objects, handling their
    creation, storage, and updates. It maintains separate paths for static and
    animated sprites and provides methods to add and update sprites.

    Attributes:
        game (Game): Reference to the main game instance
        sprite_list (List[Union[SpriteObject, AnimatedSprite]]): List of all active sprites
        static_sprite_path (Path): Directory path for static sprite resources
        animated_sprite_path (Path): Directory path for animated sprite resources
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize the object handler.

        Args:
            game (Game): Reference to the main game instance
        """
        self.game = game
        self.sprite_list: List[Union[SpriteObject, AnimatedSprite]] = []
        self.static_sprite_path: Path = SPRITES_FOLDER / "static"
        self.animated_sprite_path: Path = SPRITES_FOLDER / "animated"
        add_sprite = self.add_sprite

        # Add initial static sprites
        add_sprite(
            SpriteObject(
                self.game,
                str(self.static_sprite_path / "candlebra.png"),
                (1.5, 5),
                0.7,
                0.27,
            )
        )

        # Add initial animated sprites
        add_sprite(
            AnimatedSprite(
                self.game,
                str(self.animated_sprite_path / "green_light" / "0.png"),
                (1.5, 5),
                scale=0.8,
                shift=0.15,
            )
        )

    def update(self) -> None:
        """
        Update all sprites in the sprite list.

        Calls the update method on each sprite in the sprite_list,
        allowing them to update their state, animation, and position.
        """
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite: Union[SpriteObject, AnimatedSprite]) -> None:
        """
        Add a new sprite to the sprite list.

        Args:
            sprite (Union[SpriteObject, AnimatedSprite]): The sprite object to add
        """
        self.sprite_list.append(sprite)
