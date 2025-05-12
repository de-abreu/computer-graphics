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


class Camera:
    """
    A class to represent a camera in a 3D scene.

    The camera can rotate, zoom, and move within the boundaries of the scene.
    Based on its position and orientation, the view and projection matrices are
    calculated.
    """
    
    _pos: vec = vec(0.0, 0.0, -3.0)
    _front: vec = vec(0.0, 0.0, 0.0)
    _up: vec = vec(0.0, 1.0, 0.0)
    _mouse_sensitivity: float = 1.0
    _fov: float = 45.0
    _pitch: float = 0.0
    _yaw: float = -90.0
    _window_width: int
    _window_height: int
    first_mouse: bool = True
    last_x: float = 0.0
    last_y: float = 0.0

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
    def fov(self) -> float:
        return self._fov

    @property
    def mouse_sensitivity(self) -> float:
        return self._mouse_sensitivity

    @property
    def pitch(self) -> float:
        return self._pitch

    @property
    def yaw(self) -> float:
        return self._yaw

    def move(self, step: float, direction: str) -> None:
        """
        Move the camera in the specified direction by the given step.

        Parameters
        ----------
        step : float
            The distance to move the camera.
        direction : str
            The direction to move the camera ('z' for forward/backward, 'x' for left/right, 'y' for up/down).

        Notes
        -----
        The camera's position is clamped to prevent it from going below ground level or beyond the sky dome.
        """
        match direction:
            case "z":
                self._pos += step * self.front
            case "x":
                self._pos += step * normalize(cross(self.front, self.up))
            case _:
                self._pos += step * self.up

        # Ensure that y-coordinate does not go below ground level
        self._pos.y = max(-2.3, self._pos.y)

        # Ensure the camera does not travel beyond the sky dome.
        if (self._pos.x**2 + self._pos.y**2 + self._pos.z**2) ** 0.5 > 40.0:
            self._pos = normalize(self._pos) * 40.0

    def process_mouse_movement(self, x_offset: float, y_offset: float) -> None:
        """
        Process mouse movement to rotate the camera.

        Parameters
        ----------
        x_offset : float
            The horizontal offset of the mouse cursor.
        y_offset : float
            The vertical offset of the mouse cursor.

        Notes
        -----
        The pitch angle is clamped between -89 and 89 degrees to prevent gimbal lock.
        """
        self._yaw += x_offset * self.mouse_sensitivity
        self._pitch += y_offset * self.mouse_sensitivity

        if self._pitch > 89.0:
            self._pitch = 89.0
        elif self._pitch < -89.0:
            self._pitch = -89.0

        self.update_orientation()

    def process_scroll_movement(self, y_offset: float):
        """
        Process scroll movement to zoom the camera.

        Parameters
        ----------
        y_offset : float
            The vertical offset of the scroll wheel.

        Notes
        -----
        The field of view is clamped between 1 and 45 degrees.
        """
        self._fov -= y_offset
        if self._fov < 1.0:
            self._fov = 1.0
        elif self._fov > 45.0:
            self._fov = 45.0

    def update_orientation(self):
        """
        Update the camera's front vector based on its current pitch and yaw angles.
        """
        yaw_rad = rad(self.yaw)
        pitch_rad = rad(self.pitch)
        front = vec()
        front.x = cos(yaw_rad * cos(pitch_rad))
        front.y = sin(pitch_rad)
        front.z = sin(yaw_rad * cos(pitch_rad))
        self._front = normalize(front)

    def view(self) -> NDArray[float32]:
        """
        Generate the view matrix for the camera.

        Returns
        -------
        NDArray[float32]
            The 4x4 view matrix.
        """
        mat_view = lookAt(self.pos, self.pos + self.front, self.up)
        return array(mat_view, dtype=float32)

    def projection(self) -> NDArray[float32]:
        """
        Generate the projection matrix for the camera.

        Returns
        -------
        NDArray[float32]
            The 4x4 projection matrix.
        """
        w, h = self._window_width, self._window_height
        mat_projection = perspective(rad(self.fov), w / h, 0.1, 100.0)
        return array(mat_projection, dtype=float32)
