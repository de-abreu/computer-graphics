# Reimmplementation of the Everforest Dark Soft colorscheme.
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
        default_factory=lambda: (
            0xB3 / 255,
            0x27 / 255,
            0x27 / 255,
        )  # Darker, richer red
    )
    yellow: tuple[float, float, float] = field(
        default_factory=lambda: (
            0x9A / 255,
            0x86 / 255,
            0x17 / 255,
        )  # Deep golden yellow
    )
    blue: tuple[float, float, float] = field(
        default_factory=lambda: (
            0x1E / 255,
            0x5F / 255,
            0x8B / 255,
        )  # Darker, bluer shade
    )
    magenta: tuple[float, float, float] = field(
        default_factory=lambda: (
            0x8B / 255,
            0x0A / 255,
            0x6B / 255,
        )  # Deep plum/magenta
    )
