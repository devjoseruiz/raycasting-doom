"""
Game Configuration Settings

This module contains all the constant values and configuration parameters
used throughout the game, including display settings, player attributes,
and game mechanics constants.
"""

import math
from typing import Tuple

# Display settings
WIDTH, HEIGHT = 1600, 900  # Screen resolution
RES: Tuple[int, int] = WIDTH, HEIGHT
FPS: int = 60  # Frames per second cap

# Player settings
PLAYER_POS: Tuple[float, float] = 1.5, 5  # Initial player position (x, y)
PLAYER_ANGLE: float = 0  # Initial player viewing angle (in radians)
PLAYER_SPEED: float = 0.004  # Player movement speed multiplier
PLAYER_ROT_SPEED: float = 0.05  # Player rotation speed multiplier

# Raycasting settings
FOV = math.pi / 3  # Field of view angle
HALF_FOV = FOV / 2  # Half of the field of view
NUM_RAYS = WIDTH // 2  # Number of rays
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS  # Angle between each ray
MAX_DEPTH = 20  # Maximum depth of the raycast
