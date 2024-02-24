"""
Rubik's cube package, containing classes to mimic the use of a 3x3x3 cube
"""
__all__ = ["RubiksCube", "Color", "CubeFace", "CubeSection"]

from .cube import RubiksCube
from .notations import Color, CubeFace, CubeSection
