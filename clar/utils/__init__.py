"""Utility functions for CLAR"""

import numpy as np
from typing import Tuple


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Convert RGB color to hexadecimal.
    
    Args:
        rgb: RGB tuple (r, g, b)
        
    Returns:
        Hexadecimal color string
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hexadecimal color to RGB.
    
    Args:
        hex_color: Hexadecimal color string (e.g., '#FF5733')
        
    Returns:
        RGB tuple
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def calculate_color_distance(color1: Tuple[int, int, int], 
                             color2: Tuple[int, int, int]) -> float:
    """
    Calculate the Euclidean distance between two colors.
    
    Args:
        color1: First RGB color
        color2: Second RGB color
        
    Returns:
        Distance between colors
    """
    return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def normalize_measurements(measurements: dict) -> dict:
    """
    Normalize body/garment measurements to a standard scale.
    
    Args:
        measurements: Dictionary of measurements
        
    Returns:
        Normalized measurements
    """
    normalized = {}
    for key, value in measurements.items():
        if isinstance(value, (int, float)):
            # Convert to float and ensure positive
            normalized[key] = max(0.0, float(value))
        else:
            normalized[key] = value
    return normalized


def interpolate_colors(color1: Tuple[int, int, int], 
                       color2: Tuple[int, int, int], 
                       steps: int = 5) -> list:
    """
    Generate a gradient between two colors.
    
    Args:
        color1: Starting RGB color
        color2: Ending RGB color
        steps: Number of intermediate colors
        
    Returns:
        List of interpolated colors
    """
    gradient = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        color = tuple(
            int(c1 + (c2 - c1) * t) 
            for c1, c2 in zip(color1, color2)
        )
        gradient.append(color)
    return gradient
