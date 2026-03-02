"""Provides a standardized, immutable library of colors for use across the application.

This module defines and builds a hierarchical color standard object that can be
easily imported and used. It is designed to be read-only to ensure color
consistency.

Sample Usage:
    from cfuncs.color_standards import color_standard

    # Access hex, rgb, or hsl values for any defined color
    army_green_hex = color_standard.branch.army.hex
    marines_red_rgb = color_standard.branch.marines.rgb
    performance_yellow_hsl = color_standard.performance.yellow.hsl

    print(f"The hex code for the Army color is: {army_green_hex}")
"""

from dataclasses import dataclass, make_dataclass, field
from typing import List, Dict, Any

@dataclass(frozen=True)
class Color:
    hex: str
    rgb: List[int]
    hsl: List[int]

COLOR_DATA = [
    # Category,      Name,     Hex,      RGB,           HSL
    ['performance', 'green',  '#008000', [0, 128, 0],   [120, 100, 25]],
    ['performance', 'yellow', '#FFFF00', [255, 255, 0], [60, 100, 50]],
    ['performance', 'red',    '#FF0000', [255, 0, 0],   [0, 100, 50]],
    ['performance', 'black',  '#000000', [0, 0, 0],     [0, 0, 0]],
    ['performance', 'low visibility', '#A020F0', [160, 32, 240], [277, 87, 53]],

    ['segment', 'source',      '#A52A2A', [165, 42, 42],  [0, 59, 41]],
    ['segment', 'supplier',    '#808080', [128, 128, 128], [0, 0, 50]],
    ['segment', 'transporter', '#0072BB', [0, 114, 187], [203, 100, 37]],
    ['segment', 'theater',     '#4B5320', [75, 83, 32],   [69, 44, 23]],

    ['branch', 'army',      '#4B5320', [75, 83, 32],    [69, 44, 23]],
    ['branch', 'air force', '#5D8AA8', [93, 138, 168], [204, 29, 51]],
    ['branch', 'navy',      '#000080', [0, 0, 128],     [240, 100, 25]],
    ['branch', 'marines',   '#C41E3A', [196, 30, 58],  [350, 74, 44]],
]

def build_color_library(data: List[List[Any]]) -> Any:

    processed_data: Dict[str, Dict[str, Color]] = {}
    for category, name, hex_val, rgb_val, hsl_val in data:
        category_attr = category.replace(' ', '_')
        name_attr = name.replace(' ', '_')
        if category_attr not in processed_data:
            processed_data[category_attr] = {}
        processed_data[category_attr][name_attr] = Color(hex=hex_val, rgb=rgb_val, hsl=hsl_val)
        
    category_instances = {}
    for category_name, colors in processed_data.items():
        fields = [(name, Color) for name in colors.keys()]
        CategoryDataclass = make_dataclass(
            category_name.capitalize(), fields, frozen=True
        )
        category_instances[category_name] = CategoryDataclass(**colors)
        
    LibraryDataclass = make_dataclass(
        'ColorLibrary',
        [(name, type(instance)) for name, instance in category_instances.items()],
        frozen=True
    )
    
    return LibraryDataclass(**category_instances)


color_standard = build_color_library(COLOR_DATA)
