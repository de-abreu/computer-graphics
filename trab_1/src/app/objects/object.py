from typing import Any, Callable, override
from collections.abc import Iterable, Mapping
from glfw import ctypes
from numpy import array, cos, float32, sin
from numpy.typing import NDArray
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_DYNAMIC_DRAW,
    GL_FLOAT,
    glBufferData,
    glEnableVertexAttribArray,
    glGetAttribLocation,
    glGetUniformLocation,
    glVertexAttribPointer,
)


# Custom dictionary that triggers a callback on setitem
class TransformDict(dict[str, float]):
    _on_change: Callable[[], None] | None

    def __init__(
        self,
        *args: Iterable[tuple[str, float]] | Mapping[str, float],
        on_change: Callable[[], None] | None = None,
        **kwargs: float,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._on_change = on_change

    @override
    def __setitem__(self, key: str, value: float) -> None:
        super().__setitem__(key, value)
        if self._on_change:
            self._on_change()

    @override
    def update(self, *args: Any, **kwargs: float) -> None:
        if len(args) > 1:
            raise TypeError(f"update expected at most 1 argument, got {len(args)}")

        if args:
            other = args[0]
            if isinstance(other, Mapping):
                for key in other:
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value

        if self._on_change:
            self._on_change()


class Object:
    vertices: NDArray[float32]
    _position: TransformDict
    _initial_position: TransformDict
    _rotation: TransformDict
    _initial_rotation: TransformDict
    _scale: float
    _initial_scale: float
    loc: int
    loc_transformation: int
    transformation: NDArray[float32]

    def __init__(
        self,
        shape: list[tuple[float, float, float]],
        position: tuple[float, float, float],
        rotation: tuple[float, float, float],
        scale: float,
        program: Any,
    ):
        self.vertices = array(shape, dtype=float32)
        self._position = self._initial_position = TransformDict(
            {"x": position[0], "y": position[1], "z": position[2]},
            on_change=self.update,
        )
        self._rotation = self._initial_rotation = TransformDict(
            {"x": rotation[0], "y": rotation[1], "z": rotation[2]},
            on_change=self.update,
        )
        self._scale = self._initial_scale = scale

        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)

        # OpenGL setup
        self.loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(self.loc)
        glVertexAttribPointer(self.loc, 3, GL_FLOAT, False, stride, offset)
        self.loc_transformation = glGetUniformLocation(program, "mat_transformation")

        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW
        )

        self.update()

    # --- Properties ---
    @property
    def position(self) -> TransformDict:
        return self._position

    @position.setter
    def position(self, value: dict[str, float]):
        self._position.update(value)

    @property
    def rotation(self) -> TransformDict:
        return self._rotation

    @rotation.setter
    def rotation(self, value: dict[str, float]):
        self._rotation.update(value)

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self.update()

    def reset(self):
        self._position = self._initial_position
        self._rotation = self._initial_rotation
        self._scale = self._initial_scale
        self.update()

    def update(self):
        def rotationMatrix(rotation: TransformDict, axis: str):
            c = cos(rotation[axis])
            s = sin(rotation[axis])
            matrix = []
            match axis:
                case "x":
                    matrix = [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, c, -s, 0.0],
                        [0.0, s, c, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                case "y":
                    matrix = [
                        [c, 0.0, s, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [-s, 0.0, c, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                case _:
                    matrix = [
                        [c, -s, 0.0, 0.0],
                        [s, c, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
            return array(matrix, dtype=float32)

        s = self.scale
        scale = array(
            [
                [s, 0.0, 0.0, 0.0],
                [0.0, s, 0.0, 0.0],
                [0.0, 0.0, s, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=float32,
        )

        p = self.position
        translation = array(
            [
                [1.0, 0.0, 0.0, p["x"]],
                [0.0, 1.0, 0.0, p["y"]],
                [0.0, 0.0, 1.0, p["z"]],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=float32,
        )

        self.transformation = (
            translation
            @ rotationMatrix(self.rotation, "x")
            @ rotationMatrix(self.rotation, "y")
            @ rotationMatrix(self.rotation, "z")
            @ scale
        ).T.astype(float32)
