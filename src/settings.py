"""
Game Configuration Settings

This module contains all the constant values and configuration parameters
used throughout the game, including display settings, player attributes,
and game mechanics constants.
"""

import math
from pathlib import Path
from typing import Tuple

# Display settings
WIDTH, HEIGHT = 1600, 900  # Screen resolution
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
RES: Tuple[int, int] = WIDTH, HEIGHT
FPS: int = 60  # Frames per second cap

# Player settings
PLAYER_POS: Tuple[float, float] = 1.5, 5  # Initial player position (x, y)
PLAYER_ANGLE: float = 0  # Initial player viewing angle (in radians)
PLAYER_SPEED: float = 0.004  # Player movement speed multiplier
PLAYER_ROT_SPEED: float = 0.05  # Player rotation speed multiplier
PLAYER_SIZE_SCALE: float = 60

# Raycasting settings
FOV: float = math.pi / 3  # Field of view angle
HALF_FOV: float = FOV / 2  # Half of the field of view
NUM_RAYS: int = WIDTH // 2  # Number of rays
HALF_NUM_RAYS: int = NUM_RAYS // 2
DELTA_ANGLE: float = FOV / NUM_RAYS  # Angle between each ray
MAX_DEPTH: int = 30  # Maximum depth of the raycast
FOG_START: int = 20  # Distance at which fog starts
FOG_END: int = MAX_DEPTH  # Distance at which fog is fully opaque

SCREEN_DIST: float = HALF_WIDTH / math.tan(HALF_FOV)
SCALE: float = WIDTH // NUM_RAYS  # Scale factor

# Resources settings
BASE_PATH = Path(__file__).parent.parent
TEXTURES_FOLDER = str(BASE_PATH / "resources" / "textures")

# Texture settings
TEXTURE_SIZE: int = 256
HALF_TEXTURE_SIZE: int = TEXTURE_SIZE // 2
FLOOR_COLOR = (30, 30, 30)
