# Implementation of the Everforest Dark Soft colorscheme.
# Source:
# https://github.com/Gogh-Co/Gogh/blob/master/themes/Everforest%20Dark%20Soft.yml

from dataclasses import dataclass, field


@dataclass
class Palette:
    # Color values are scaled to [0, 1]
    background: tuple[float, float, float] = field(
        default_factory=lambda: (0x33 / 255, 0x3C / 255, 0x43 / 255)
    )
    white: tuple[float, float, float] = field(
        default_factory=lambda: (0xD3 / 255, 0xC6 / 255, 0xAA / 255)
    )
    green: tuple[float, float, float] = field(
        default_factory=lambda: (0xA7 / 255, 0xC0 / 255, 0x80 / 255)
    )
    red: tuple[float, float, float] = field(
        default_factory=lambda: (0xE6 / 255, 0x7E / 255, 0x80 / 255)
    )
    yellow: tuple[float, float, float] = field(
        default_factory=lambda: (0xDB / 255, 0xBC / 255, 0x7F / 255)
    )
    blue: tuple[float, float, float] = field(
        default_factory=lambda: (0x7F / 255, 0xBB / 255, 0xB3 / 255)
    )
    magenta: tuple[float, float, float] = field(
        default_factory=lambda: (0xD6 / 255, 0x99 / 255, 0xB6 / 255)
    )
