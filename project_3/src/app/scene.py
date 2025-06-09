import ctypes
from numpy import array, float32
from app.camera import Camera
from app.object import Object
from app.light_source import Light
from app.utils import (
    BufferData,
    IlluminationProperties,
    Location,
    ObjectConfig,
    ReflectionCoefficients,
    Shader,
)
from dataclasses import asdict
import toml
import os
from typing import Any
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_BLEND,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_DONT_CARE,
    GL_FLOAT as FLOAT,
    GL_LINE_SMOOTH,
    GL_LINE_SMOOTH_HINT,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_SRC_ALPHA,
    GL_STATIC_DRAW,
    GL_TEXTURE_2D,
    GL_TRIANGLES as TRIANGLES,
    GL_TRUE as TRUE,
    glBindBuffer,
    glBindTexture,
    glBlendFunc,
    glBufferData,
    glClear,
    glClearColor,
    glDrawArrays,
    glEnable,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGetAttribLocation,
    glGetUniformLocation,
    glHint,
    glUniform1i,
    glUniform1f,
    glUniform3f,
    glUniformMatrix4fv,
    glVertexAttribPointer,
)
from glfw import (
    get_window_size,
    show_window,
    swap_buffers,
)


class Scene:
    """
    A class to represent a 3D scene containing objects, light sources, and a camera.

    Attributes
    ----------
    camera : Camera
        The camera viewing the scene.
    program : Any
        The OpenGL shader program ID.
    window : Any
        The GLFW window object.
    objects : list[Object]
        The list of 3D objects in the scene.
    light_sources : list[Light]
        The list of light sources in the scene.
    num_lights : int
        The number of light sources in the scene (default: 3).
    ambient_light_on : bool
        Flag to toggle ambient lighting (default: True).

    Methods
    -------
    __init__(window: Any, config_path: str) -> None
        Initialize the scene with objects loaded from a TOML configuration file.
    draw() -> None
        Render the scene.
    """

    camera: Camera
    program: Any
    window: Any
    _objects: list[Object] = []
    _light_sources: list[Light] = []
    ambient_light_on: bool = True

    def __init__(self, window: Any, config_path: str) -> None:
        """
        Initialize the scene with objects loaded from a TOML configuration file.

        Parameters
        ----------
        window : Any
            The GLFW window object.
        config_path : str
            Path to the TOML configuration file.
        """

        shader = Shader("src/shaders/vertex.vs", "src/shaders/fragments.fs")
        width, height = get_window_size(window)
        bd = BufferData()
        self.camera = Camera(width, height)
        self.program = shader.getProgram()
        self.window = window
        descriptors = self._load_config(config_path)
        for i, desc in enumerate(descriptors):
            if desc.illumination_properties.emission_intensity > 0.01:
                light = Light(i, desc, bd)
                self._objects.append(light)
                self._light_sources.append(light)
            else:
                self._objects.append(Object(i, desc, bd))

        shader.use()
        self._init_buffers(bd)
        self._init_light_sources()
        glEnable(GL_TEXTURE_2D)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        show_window(window)
        glEnable(GL_DEPTH_TEST)

    @property
    def objects(self) -> list[Object]:
        return self._objects

    @property
    def light_sources(self) -> list[Light]:
        return self._light_sources

    def _init_buffers(self, bd: BufferData):
        buffers = glGenBuffers(3)
        self._upload_data(buffers[0], bd.vertices, 3, "position")
        self._upload_data(buffers[1], bd.texture_coord, 2, "texture_coord")
        self._upload_data(buffers[2], bd.normals, 3, "normals")

    def _upload_data(
        self,
        buffer: Any,
        coord_list: list[tuple[float, ...]],
        coord_size: int,
        attr_name: str,
    ) -> None:
        """
        Upload vertex data to the GPU.

        Parameters
        ----------
        vertices_list : list[tuple[float, float, float]]
            List of vertex coordinates (x, y, z).
        buffer : Any
            The OpenGL buffer ID for vertex data.
        """
        coords = array(coord_list, dtype=float32)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_STATIC_DRAW)
        stride, offset = coords.strides[0], ctypes.c_void_p(0)
        loc = glGetAttribLocation(self.program, attr_name)
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, coord_size, FLOAT, False, stride, offset)

    def _init_light_sources(self) -> None:
        for i, light in enumerate(self._light_sources):
            loc = glGetUniformLocation(self.program, f"lights[{i}].color")
            glUniform3f(loc, *light.illumination.emission_color)
            loc = glGetUniformLocation(self.program, f"lights[{i}].location")
            glUniform1i(loc, light.location)

    def _load_config(self, config_path: str) -> list[ObjectConfig]:
        """
        Load the scene configuration from a TOML file.

        Parameters
        ----------
        config_path : str
            Path to the TOML configuration file.

        Returns
        -------
        list[ObjectConfig]
            A list of ObjectConfig objects.
        """
        with open(config_path, "r") as f:
            config = toml.load(f)

        path = os.path.dirname(config_path)
        return [
            ObjectConfig(
                path,
                name,
                tuple(props.get("position", (0.0, 0.0, -20.0))),
                tuple(props.get("rotation", (0.0, 0.0, 0.0))),
                props.get("scale", 1.0),
                IlluminationProperties(
                    ReflectionCoefficients(
                        props.get("ambient_intensity", 0.5),
                        props.get("diffuse_intensity", 0.5),
                        props.get("specular_intensity", 0.5),
                        props.get("specular_expoent", 32.0),
                    ),
                    props.get("emission_intensity", 0.0),
                    tuple(props.get("ambient_color", (1.0, 1.0, 1.0))),
                    tuple(props.get("emission_color", (1.0, 1.0, 1.0))),
                ),
                Location[props.get("location", "both")],
            )
            for name, props in config.items()
        ]

    def draw(self) -> None:
        """
        Render the scene.

        Returns
        -------
        None
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0x33 / 255, 0x3C / 255, 0x43 / 255, 1.0)

        # Send camera position
        loc = glGetUniformLocation(self.program, "viewPos")
        glUniform3f(loc, *self.camera.pos)

        # Set point light sources
        for i, light in enumerate(self._light_sources):
            loc = glGetUniformLocation(self.program, f"lights[{i}].intensity")
            glUniform1f(loc, light.intensity)
            loc = glGetUniformLocation(self.program, f"lights[{i}].position")
            pos = light.position
            glUniform3f(loc, pos["x"], pos["y"], pos["z"])

        # Set objects
        for obj in self._objects:
            # Set illumination parameters
            for coefficient, value in asdict(
                obj.illumination.reflection_coefficients
            ).items():
                loc = glGetUniformLocation(self.program, coefficient)
                glUniform1f(loc, value)

            if not self.ambient_light_on:
                loc = glGetUniformLocation(self.program, "ambient_intensity")
                glUniform1f(loc, 0.0)

            loc = glGetUniformLocation(self.program, "ambient_color")
            glUniform3f(loc, *obj.illumination.ambient_color)

            loc = glGetUniformLocation(self.program, "is_emitter")
            if isinstance(obj, Light):
                glUniform1i(loc, obj.on)
                loc = glGetUniformLocation(self.program, "emission_color")
                glUniform3f(loc, *obj.illumination.emission_color)
            else:
                glUniform1i(loc, False)

            # Set model parameters
            loc = glGetUniformLocation(self.program, "object_location")
            glUniform1i(loc, obj.location)

            loc = glGetUniformLocation(self.program, "model")
            glUniformMatrix4fv(loc, 1, TRUE, obj.transformation)

            glBindTexture(GL_TEXTURE_2D, obj.id)
            glDrawArrays(TRIANGLES, obj.initial_vertex, obj.vertices_count)

        # Apply view and porjection matrix multiplications and render
        loc = glGetUniformLocation(self.program, "view")
        glUniformMatrix4fv(loc, 1, TRUE, self.camera.view())
        loc = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(loc, 1, TRUE, self.camera.projection())
        swap_buffers(self.window)
