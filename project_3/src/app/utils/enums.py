from enum import IntEnum


class Location(IntEnum):
    internal = 0
    external = 1
    both = 2


class Mode(IntEnum):
    camera = 0
    translating = 1
    rotating = 2
    scaling = 3
    light = 4
