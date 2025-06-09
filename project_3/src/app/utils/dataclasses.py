from dataclasses import dataclass, field
from .enums import Location

@dataclass
class ReflectionCoefficients:
    ambient_intensity: float
    diffuse_intensity: float
    specular_intensity: float
    specular_exponent: float


@dataclass
class IlluminationProperties:

    reflection_coefficients: ReflectionCoefficients

    # Light emission
    emission_intensity: float

    # Light color
    ambient_color: tuple[float, float, float]
    emission_color: tuple[float, float, float]


@dataclass
class ObjectConfig:
    """
    A configuration class for object properties.

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

    path: str
    model_name: str
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: float
    illumination_properties: IlluminationProperties
    location: Location = Location.both


@dataclass
class BufferData:
    vertices: list[tuple[float, float, float]] = field(default_factory=list)
    normals: list[tuple[float, float, float]] = field(default_factory=list)
    texture_coord: list[tuple[float, float]] = field(default_factory=list)


@dataclass
class Face:
    vertices: list[int] = field(default_factory=list)
    texture: list[int] = field(default_factory=list)
    normals: list[int] = field(default_factory=list)
    material: str | None = None


@dataclass
class Model(BufferData):
    """
    A dataclass representing a 3D model.

    Attributes
    ----------
    vertices : list[tuple[float, float, float]]
        The vertices of the model.
    texture_coord : list[tuple[float, float]]
        The texture coordinates of the model.
    faces : list[tuple[list[int], list[int], str | None]]
        The faces of the model, including vertex indices, texture indices, and material names.
    """

    faces: list[Face] = field(default_factory=list)
