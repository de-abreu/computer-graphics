from glob import glob
from app.transform_dict import TransformDict
from copy import deepcopy
from OpenGL.GL.images import glTexImage2D
from OpenGL.constants import GL_UNSIGNED_BYTE
from PIL import Image
from typing import TypedDict, final
from OpenGL.GL import (
    GL_LINEAR,
    GL_REPEAT,
    GL_RGB,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    glTexParameteri,
    glBindTexture,
)
from numpy import array, cos, float32, sin
from numpy.typing import NDArray


@final
class ObjDescriptor:
    """
    A descriptor class for object properties.

    Attributes
    ----------
    model_name : str
        The name of the 3D model, must match a folder name under src/objects.
    initial_position : tuple[float, float, float]
        The initial position of the object in 3D space.
    initial_rotation : tuple[float, float, float]
        The initial rotation of the object in radians.
    initial_scale : float
        The initial scale of the object.
    """

    def __init__(
        self,
        model_name: str,
        initial_position: tuple[float, float, float] = (0.0, 0.0, -20.0),
        initial_rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
        initial_scale: float = 1.0,
    ):
        self.model_name = model_name
        self.initial_position = initial_position
        self.initial_rotation = initial_rotation
        self.initial_scale = initial_scale


class Model(TypedDict):
    """
    A typed dictionary representing a 3D model.

    Attributes
    ----------
    vertices : list[tuple[float, float, float]]
        The vertices of the model.
    texture_coord : list[tuple[float, float]]
        The texture coordinates of the model.
    faces : list[tuple[list[int], list[int], str | None]]
        The faces of the model, including vertex indices, texture indices, and material names.
    """

    vertices: list[tuple[float, float, float]]
    texture_coord: list[tuple[float, float]]
    faces: list[tuple[list[int], list[int], str | None]]


class Object:
    """
    A class to represent a 3D object in the scene.

    Attributes
    ----------
    _name : str
        The name of the object.
    _id : int
        The unique identifier of the object.
    _initial_vertex : int
        The starting index of the object's vertices in the global vertex list.
    _vertices_count : int
        The number of vertices in the object.
    _initial_position : TransformDict
        The initial position of the object.
    _initial_rotation : TransformDict
        The initial rotation of the object.
    _initial_scale : float
        The initial scale of the object.
    _position : TransformDict
        The current position of the object.
    _rotation : TransformDict
        The current rotation of the object.
    _scale : float
        The current scale of the object.
    _transformation : NDArray[float32]
        The transformation matrix of the object.
    """

    _name: str
    _id: int
    _initial_vertex: int
    _vertices_count: int
    _initial_position: TransformDict
    _initial_rotation: TransformDict
    _initial_scale: float
    _position: TransformDict
    _rotation: TransformDict
    _scale: float
    _transformation: NDArray[float32]

    def __init__(
        self,
        id: int,
        description: ObjDescriptor,
        vertices: list[tuple[float, float, float]],
        texture_coord: list[tuple[float, float]],
    ):
        self._id = id
        self._name = description.model_name
        self._initial_vertex, self._vertices_count = self._load_object(
            vertices, texture_coord
        )

        pos = description.initial_position
        self._initial_position = TransformDict(
            {"x": pos[0], "y": pos[1], "z": pos[2]},
            on_change=self.update,
        )
        self._position = deepcopy(self._initial_position)

        rot = description.initial_rotation
        self._initial_rotation = TransformDict(
            {"x": rot[0], "y": rot[1], "z": rot[2]},
            on_change=self.update,
        )
        self._rotation = deepcopy(self._initial_rotation)
        self._scale = self._initial_scale = description.initial_scale
        self.update()

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @property
    def initial_vertex(self) -> int:
        return self._initial_vertex

    @property
    def vertices_count(self) -> int:
        return self._vertices_count

    @property
    def transformation(self) -> NDArray[float32]:
        return self._transformation

    @property
    def position(self) -> TransformDict:
        return self._position

    @position.setter
    def position(self, value: dict[str, float]):  # pyright: ignore[reportPropertyTypeMismatch]
        self._position.update(value)

    @property
    def rotation(self) -> TransformDict:
        return self._rotation

    @rotation.setter
    def rotation(self, value: dict[str, float]):  # pyright: ignore[reportPropertyTypeMismatch]
        self._rotation.update(value)

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = max(0.01, value)
        self.update()

    def _load_model(self) -> Model:
        """
        Load the 3D model from an OBJ file.

        Returns
        -------
        Model
            A dictionary containing the vertices, texture coordinates, and faces of the model.

        Notes
        -----
        The OBJ file is expected to be in the `src/objects/{model_name}/model.obj` path.
        """
        model: Model = {"vertices": [], "texture_coord": [], "faces": []}
        material: str | None = None

        for line in open(f"src/objects/{self._name}/model.obj", "r"):
            if line.startswith("#"):
                continue
            values = line.split()
            if not values:
                continue
            match values[0]:
                case "v":  # recovering vertices
                    model["vertices"].append(
                        (float(values[1]), float(values[2]), float(values[3]))
                    )
                case "vt":  # recovering texture coordinates
                    model["texture_coord"].append(
                        (float(values[1]), float(values[2]))
                    )
                case "f":
                    face: list[int] = []
                    face_texture: list[int] = []
                    for v in values[1:]:
                        w: list[str] = v.split("/")
                        face.append(int(w[0]))
                        if len(w) >= 2 and len(w[1]) > 0:
                            face_texture.append(int(w[1]))
                        else:
                            face_texture.append(0)
                    model["faces"].append((face, face_texture, material))
                case "usemtl" | "usemat":
                    material = values[1]
                case _:
                    pass
        return model

    def _load_texture(self):
        """
        Load and bind the texture for the object.

        Notes
        -----
        The texture file is expected to be in the `src/objects/{model_name}/texture.*` path.
        """
        glBindTexture(GL_TEXTURE_2D, self._id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        img = Image.open(glob(f"src/objects/{self._name}/texture.*")[0])
        width = img.size[0]
        height = img.size[1]
        img_data = img.tobytes("raw", "RGB", 0, -1)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            img_data,
        )

    @staticmethod
    def _triangulate_face(face: list[int]) -> list[int]:
        """
        Convert a face into a set of triangles using fan triangulation.

        Parameters
        ----------
        face : list[int]
            The indices of the vertices forming the face.

        Returns
        -------
        list[int]
            The indices of the vertices forming the triangulated face.
        """
        triangulated_face: list[int] = []
        for i in range(1, len(face) - 1):
            triangulated_face.extend([face[0], face[i], face[i + 1]])
        return triangulated_face

    def _load_object(
        self,
        vertices_list: list[tuple[float, float, float]],
        texture_coord_list: list[tuple[float, float]],
    ) -> tuple[int, int]:
        """
        Load the object's vertices and texture coordinates into the global lists.

        Parameters
        ----------
        vertices_list : list[tuple[float, float, float]]
            The global list of vertices.
        texture_coord_list : list[tuple[float, float]]
            The global list of texture coordinates.

        Returns
        -------
        tuple[int, int]
            The starting index and count of the object's vertices in the global list.
        """
        model = self._load_model()
        start = len(vertices_list)

        for face in model["faces"]:
            for vertex_id in Object._triangulate_face(face[0]):
                vertices_list.append(model["vertices"][vertex_id - 1])
            for texture_id in Object._triangulate_face(face[1]):
                texture_coord_list.append(
                    model["texture_coord"][texture_id - 1]
                )
        self._load_texture()

        return start, len(vertices_list) - start

    def reset(self) -> None:
        """
        Reset the object to its initial position, rotation, and scale.
        """
        self._position = deepcopy(self._initial_position)
        self._rotation = deepcopy(self._initial_rotation)
        self._scale = self._initial_scale
        self.update()

    def _rotationMatrix(self, axis: str) -> NDArray[float32]:
        """
        Generate a rotation matrix for the specified axis.

        Parameters
        ----------
        axis : str
            The axis of rotation ('x', 'y', or 'z').

        Returns
        -------
        NDArray[float32]
            The 4x4 rotation matrix.
        """
        c = cos(self.rotation[axis])
        s = sin(self.rotation[axis])
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
        Update the object's transformation matrix based on its current position, rotation, and scale.
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

        self._transformation = (
            translation
            @ self._rotationMatrix("z")
            @ self._rotationMatrix("y")
            @ self._rotationMatrix("x")
            @ scale
        ).astype(float32)
