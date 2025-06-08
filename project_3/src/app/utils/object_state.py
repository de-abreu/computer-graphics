from copy import copy
from typing import Callable
from .transform_dict import TransformDict


class ObjectState:
    position: dict[str, float]
    rotation: dict[str, float]
    scale: float

    def __init__(
        self,
        position: tuple[float, float, float],
        rotation: tuple[float, float, float],
        scale: float,
        callback: Callable[[], None],
    ):
        self.position = TransformDict(
            {key: value for key, value in zip(("x", "y", "z"), position)},
            on_change=callback,
        )
        self.rotation = TransformDict(
            {key: value for key, value in zip(("x", "y", "z"), rotation)},
            on_change=callback,
        )
        self.scale = scale

    def copy(self, other: "ObjectState"):
        """Copy the state from another ObjectState instance deeply."""
        self.position = copy(other.position)
        self.rotation = copy(other.rotation)
        self.scale = other.scale
