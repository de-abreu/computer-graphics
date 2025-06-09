from glob import glob
from app.utils import (
    BufferData,
    Face,
    Location,
    Model,
    ObjectConfig as Config,
    ObjectState as State,
    IlluminationProperties,
)
from OpenGL.GL.images import glTexImage2D
from OpenGL.constants import GL_UNSIGNED_BYTE
from PIL import Image
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


class Object:
    """
    A class representing a 3D object in the scene.
    """
    name: str
    location: Location
    illumination: IlluminationProperties
    _id: int
    _initial_vertex: int
    _vertices_count: int
    _initial: State
    _current: State
    _transformation: NDArray[float32]

    def __init__(self, id: int, config: Config, bd: BufferData):
        """Initialize the object with a unique ID, configuration, and buffer data.

        Parameters
        ----------
        id : int
            The unique identifier for the object.
        config : Config
            The configuration for the object (e.g., model name, path, illumination).
        bd : BufferData
            The buffer data for storing vertices, texture coordinates, and normals.
        """
        self._id = id
        self.name = config.model_name
        self.location = config.location
        self.illumination = config.illumination_properties
        self._initial_vertex, self._vertices_count = self._load_object(
            f"{config.path}/{config.model_name}", bd
        )
        parameters = {
            "position": config.position,
            "rotation": config.rotation,
            "scale": config.scale,
            "callback": self._update
        }
        self._initial = State(**parameters)  # pyright: ignore [reportArgumentType]
        self._current = State(**parameters)  # pyright: ignore [reportArgumentType]
        self._update()


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
    def position(self) -> dict[str, float]:
        return self._current.position

    @position.setter
    def position(self, value: dict[str, float]):
        self._current.position = value

    @property
    def rotation(self) -> dict[str, float]:
        return self._current.rotation

    @rotation.setter
    def rotation(self, value: dict[str, float]):
        self._current.rotation = value

    @property
    def scale(self) -> float:
        return self._current.scale

    @scale.setter
    def scale(self, value: float):
        self._current.scale = max(0.01, value)
        self._update()

    def _load_model(self, path: str) -> Model:
        model = Model()
        material: str | None = None

        for line in open(f"{path}/model.obj", "r"):
            if line.startswith("#"):
                continue
            values = line.split()
            if not values:
                continue
            match values[0]:
                case "v":
                    model.vertices.append(
                        (float(values[1]), float(values[2]), float(values[3]))
                    )
                case "vt":
                    model.texture_coord.append(
                        (float(values[1]), float(values[2]))
                    )
                case "vn":
                    model.normals.append(
                        (float(values[1]), float(values[2]), float(values[3]))
                    )
                case "f":
                    face = Face(material=material)
                    for v in values[1:]:
                        w: list[str] = v.split("/")
                        face.vertices.append(int(w[0]))
                        if len(w) >= 2 and len(w[1]) > 0:
                            face.texture.append(int(w[1]))
                        else:
                            face.texture.append(0)
                        face.normals.append(int(w[2]))
                    model.faces.append(face)
                case "usemtl" | "usemat":
                    material = values[1]
                case _:
                    pass
        return model

    def _load_texture(self, path: str):
        glBindTexture(GL_TEXTURE_2D, self._id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        img = Image.open(glob(f"{path}/texture.*")[0])
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
        triangulated_face: list[int] = []
        for i in range(1, len(face) - 1):
            triangulated_face.extend([face[0], face[i], face[i + 1]])
        return triangulated_face

    def _load_object(self, path: str, bd: BufferData) -> tuple[int, int]:
        model = self._load_model(path)
        start = len(bd.vertices)
        for face in model.faces:
            for vertex_id in Object._triangulate_face(face.vertices):
                bd.vertices.append(model.vertices[vertex_id - 1])
            for texture_id in Object._triangulate_face(face.texture):
                bd.texture_coord.append(model.texture_coord[texture_id - 1])
            for normal_id in Object._triangulate_face(face.normals):
                bd.normals.append(model.normals[normal_id - 1])
        self._load_texture(path)

        return start, len(bd.vertices) - start

    def reset(self) -> None:
        """
        Reset the object to its initial position, rotation, and scale.
        """
        self._current.copy(self._initial)

    def _rotationMatrix(self, axis: str) -> NDArray[float32]:
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

    def _update(self):
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
