from copy import copy, deepcopy
from typing import Any, Callable, final, override
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


@final
class TransformDict(dict[str, float]):
    """
    A custom dictionary that triggers a callback function whenever an item is set.

    Attributes:
        _on_change (Callable[[], None] | None): A callback function to be called on item change.
    """

    _on_change: Callable[[], None] | None

    def __init__(
        self,
        *args: Iterable[tuple[str, float]] | Mapping[str, float],
        on_change: Callable[[], None] | None = None,
        **kwargs: float,
    ) -> None:
        """
        Initializes the TransformDict with optional initial values and a callback.

        Args:
            *args: Initial key-value pairs as tuples or a mapping.
            on_change (Callable[[], None], optional): A callback function to call on item change.
            **kwargs: Additional key-value pairs.
        """
        super().__init__(*args, **kwargs)
        self._on_change = on_change

    @override
    def __setitem__(self, key: str, value: float) -> None:
        """
        Sets the value for a key and triggers the on_change callback if defined.

        Args:
            key (str): The key to set.
            value (float): The value to set for the key.
        """
        super().__setitem__(key, value)
        if self._on_change:
            self._on_change()

    @override
    def update(self, *args: Any, **kwargs: float) -> None:
        """
        Updates the dictionary with key-value pairs from another mapping or iterable.

        Args:
            *args: A single mapping or iterable of key-value pairs.
            **kwargs: Additional key-value pairs to update.

        Raises:
            TypeError: If more than one positional argument is provided.
        """
        if len(args) > 1:
            raise TypeError(
                f"update expected at most 1 argument, got {len(args)}"
            )

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

    def __copy__(self) -> "TransformDict":
        new_dict = TransformDict(self, on_change=None)
        new_dict._on_change = self._on_change
        return new_dict

    def __deepcopy__(
        self, memo: dict[int, object] | None = None
    ) -> "TransformDict":
        if memo is None:
            memo = {}
        new_dict = TransformDict(self, on_change=copy(self._on_change))
        memo[id(self)] = new_dict  # helps with recursive copying
        return new_dict


class Object:
    _initial_position: TransformDict
    _initial_rotation: TransformDict
    _initial_scale: float
    _position: TransformDict
    _rotation: TransformDict
    _scale: float
    loc: int
    loc_transformation: int
    program: Any
    transformation: NDArray[float32]
    vertices: NDArray[float32]

    def __init__(
        self,
        shape: list[tuple[float, float, float]],
        position: tuple[float, float, float],
        rotation: tuple[float, float, float],
        scale: float,
        program: Any,
    ):
        self.vertices = array(shape, dtype=float32)
        self._initial_position = TransformDict(
            {"x": position[0], "y": position[1], "z": position[2]},
            on_change=self.update,
        )
        self._position = deepcopy(self._initial_position)
        self._initial_rotation = TransformDict(
            {"x": rotation[0], "y": rotation[1], "z": rotation[2]},
            on_change=self.update,
        )
        self._rotation = deepcopy(self._initial_rotation)
        self._scale = self._initial_scale = scale
        self.program = program
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
        """
        Resets the object's position, rotation, and scale to their initial values.

        Note:
            - For mutable properties (`_position`, `_rotation`), a deep copy is used to prevent
            unintended side effects if the initial values are modified externally.
            - `_scale` is directly assigned (no copy) assuming it is an immutable type (e.g., `float`).
        """
        self._position = deepcopy(self._initial_position)
        self._rotation = deepcopy(self._initial_rotation)
        self._scale = self._initial_scale
        self.update()

    def _rotationMatrix(self, axis: str):
        c = cos(self.rotation[axis])
        s = sin(self.rotation[axis])
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

    def update(self):
        """
        Updates the transformation matrix based on the current position, rotation, and scale.

        This method calculates the transformation matrix by applying translation, rotation,
        and scaling transformations in the correct order. The resulting transformation matrix
        is stored in the `transformation` attribute, which can be used for rendering the object.
        """

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
            @ self._rotationMatrix("z")
            @ self._rotationMatrix("y")
            @ self._rotationMatrix("x")
            @ scale
        ).astype(float32)

    def draw(self):
        """
        Prepares the object for rendering by setting up the necessary OpenGL state.

        This method retrieves the attribute location for the vertex data in the shader program,
        enables the vertex attribute array, and specifies the layout of the vertex data. It also
        uploads the vertex data to the GPU using a buffer.

        This method should be called before rendering the object to ensure that the OpenGL context
        is correctly set up for drawing the object.
        """
        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)

        # OpenGL setup
        self.loc = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(self.loc)
        glVertexAttribPointer(self.loc, 3, GL_FLOAT, False, stride, offset)
        self.loc_transformation = glGetUniformLocation(
            self.program, "mat_transformation"
        )
        glBufferData(
            GL_ARRAY_BUFFER,
            self.vertices.nbytes,
            self.vertices,
            GL_DYNAMIC_DRAW,
        )
