from enum import Enum
from glm import (
    cross,
    lookAt,
    normalize,
    perspective,
    radians as rad,
    vec3 as vec,
    sin,
    cos,
)
from numpy import array, float32
from numpy.typing import NDArray

Direction = Enum("Direction", ["front", "side", "up"])


class Camera:
    _pos: vec = vec(0.0, 0.0, -3.0)
    _front: vec = vec(0.0, 0.0, 0.0)
    _up: vec = vec(0.0, 1.0, 0.0)
    _first_mouse: bool = True
    _fov: float = 45.0
    _last_x: float = 0.0
    _last_y: float = 0.0
    _mouse_sensitivity: float = 0.1
    _pitch: float = 0.0
    _yaw: float = -90.0
    _window_width: int
    _window_height: int

    def __init__(self, window_width: int, window_height: int) -> None:
        self._window_width = window_width
        self._window_height = window_height
        self.update_orientation()

    @property
    def pos(self) -> vec:
        return self._pos

    @property
    def front(self) -> vec:
        return self._front

    @property
    def up(self) -> vec:
        return self._up

    @property
    def first_mouse(self) -> bool:
        return self._first_mouse

    @property
    def fov(self) -> float:
        return self._fov

    @property
    def last_x(self) -> float:
        return self._last_x

    @property
    def last_y(self) -> float:
        return self._last_y

    @property
    def mouse_sensitivity(self) -> float:
        return self._mouse_sensitivity

    @property
    def pitch(self) -> float:
        return self._pitch

    @property
    def yaw(self) -> float:
        return self._yaw

    def move(self, step: float, direction: Direction) -> None:
        match direction:
            case Direction.front:
                self._pos += step * self.front
            case Direction.side:
                self._pos += step * normalize(cross(self.front, self.up))
            case _:
                self._pos += step * self.up

    def process_mouse_movement(self, x_offset: float, y_offset: float) -> None:
        self._yaw += x_offset * self.mouse_sensitivity
        self._pitch += y_offset * self.mouse_sensitivity

        if self._pitch > 89.0:
            self._pitch = 89.0
        elif self._pitch < -89.0:
            self._pitch = -89.0

        self.update_orientation()

    def process_scroll_movement(self, y_offset: float):
        self._fov -= y_offset
        if self._fov < 1.0:
            self._fov = 1.0
        elif self._fov > 45.0:
            self._fov = 45.0

    def update_orientation(self):
        yaw_rad = rad(self.yaw)
        pitch_rad = rad(self.pitch)
        front = vec()
        front.x = cos(yaw_rad * cos(pitch_rad))
        front.y = sin(pitch_rad)
        front.z = sin(yaw_rad * cos(pitch_rad))
        self._front = normalize(front)

    def view(self) -> NDArray[float32]:
        mat_view = lookAt(self.pos, self.pos + self.front, self.up)
        return array(mat_view, dtype=float32)

    def projection(self) -> NDArray[float32]:
        w, h = self._window_width, self._window_height
        mat_projection = perspective(rad(self.fov), w / h, 0.1, 100.0)
        return array(mat_projection, dtype=float32)
