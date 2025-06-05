# pyright: reportCallIssue=false
from OpenGL.raw.GL.VERSION.GL_2_0 import glUniform1f
from app.camera import Camera
from app.object import Object
from app.utils import Shader, ObjConfig, ReflectionCoeficients
from dataclasses import asdict
import toml
import os
from typing import Any
from OpenGL.GL import (
    GL_BLEND,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_DONT_CARE,
    GL_LINE_SMOOTH,
    GL_LINE_SMOOTH_HINT,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_SRC_ALPHA,
    GL_TEXTURE_2D,
    GL_TRIANGLES as TRIANGLES,
    GL_TRUE as TRUE,
    glBindTexture,
    glBlendFunc,
    glClear,
    glClearColor,
    glDrawArrays,
    glEnable,
    glGetUniformLocation,
    glHint,
    glUniformMatrix4fv,
)
from glfw import (
    get_window_size,
    set_window_user_pointer,
    show_window,
    swap_buffers,
)
from tabulate import tabulate

from app.utils import init_buffers
from app.utils.dataclasses import BufferData


class Scene:
    """
    A class to represent a 3D scene containing objects and a camera.

    Attributes
    ----------
    camera : Camera
        The camera viewing the scene.
    program : Any
        The OpenGL shader program ID.
    objects : list[Object]
        The list of 3D objects in the scene.
    index : int
        The index of the object currently under control.
    """

    camera: Camera
    program: Any
    objects: list[Object] = []
    index: int = 0

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
        shader.use()
        glEnable(GL_TEXTURE_2D)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        width, height = get_window_size(window)
        bd = BufferData()
        self.camera = Camera(width, height)
        self.program = shader.getProgram()
        descriptors = self._load_config(config_path)
        for i, desc in enumerate(descriptors):
            self.objects.append(Object(i, desc, bd))
        init_buffers(self.program, bd)
        set_window_user_pointer(window, self)
        show_window(window)
        glEnable(GL_DEPTH_TEST)

    def _load_config(self, config_path: str) -> list[ObjConfig]:
        """
        Load the scene configuration from a TOML file.

        Parameters
        ----------
        config_path : str
            Path to the TOML configuration file.

        Returns
        -------
        list[ObjConfig]
            A list of ObjConfig objects.
        """
        with open(config_path, "r") as f:
            config = toml.load(f)

        path = os.path.dirname(config_path)
        return [
            ObjConfig(
                path,
                name,
                tuple(props.get("position", (0.0, 0.0, -20.0))),
                tuple(props.get("rotation", (0.0, 0.0, 0.0))),
                props.get("scale", 1.0),
                ReflectionCoeficients(
                    props.get("ambient", 0.5),
                    props.get("diffuse", 0.5),
                    props.get("specular", 0.5),
                    props.get("specular_expoent", 32.0),
                ),
                props.get("emmiter", None),
            )
            for name, props in config.items()
        ]

    def draw(self, window: Any) -> None:
        """
        Render the scene.

        Parameters
        ----------
        window : Any
            The GLFW window object.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0x33 / 255, 0x3C / 255, 0x43 / 255, 1.0)
        for obj in self.objects:
            mat = obj.transformation
            loc = glGetUniformLocation(self.program, "model")
            glUniformMatrix4fv(loc, 1, TRUE, mat)
            for coefficient, value in asdict(obj.rc):
                loc = glGetUniformLocation(self.program, coefficient)
                glUniform1f(loc, value)
            glBindTexture(GL_TEXTURE_2D, obj.id)
            glDrawArrays(TRIANGLES, obj.initial_vertex, obj.vertices_count)
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, "view"),
            1,
            TRUE,
            self.camera.view(),
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, "projection"),
            1,
            TRUE,
            self.camera.projection(),
        )
        swap_buffers(window)

    def objects_state(self) -> list[list[str]]:
        """
        Generate a formatted state of all objects in the scene.

        Returns
        -------
        list[list[str]]
            A table-like structure with object positions, rotations, and scales.
        """
        state: list[list[str]] = []
        for i, obj in enumerate(self.objects):
            state.append(
                [
                    f"{i + 1}",
                    f"({obj.position['x']:.2f}, {obj.position['y']:.2f}, {obj.position['z']:.2f})",
                    f"({obj.rotation['x']:.2f}, {obj.rotation['y']:.2f}, {obj.rotation['z']:.2f})",
                    f"{obj.scale:.2f}",
                ]
            )
        return state

    def camera_state(self) -> list[str]:
        """
        Generate a formatted state of the camera.

        Returns
        -------
        list[str]
            A list containing camera position, front, and up vectors.
        """
        cam = self.camera
        state: list[str] = [
            f"({cam.pos.x:.2f}, {cam.pos.y:.2f}, {cam.pos.z:.2f})",
            f"({cam.front.x:.2f}, {cam.front.y:.2f}, {cam.front.z:.2f})",
            f"({cam.up.x:.2f}, {cam.up.y:.2f}, {cam.up.z:.2f})",
        ]
        return state

    def log(self) -> None:
        """
        Print the current state of objects and camera to the console.
        Uses `tabulate` for pretty-printing.
        """
        i = self.index
        _ = os.system("clear")
        print("Objects' state")
        headers = [
            "Object",
            "Position (x, y, z)",
            "Rotation (x, y, z)",
            "Scale",
        ]
        print(tabulate(self.objects_state(), headers=headers, tablefmt="grid"))
        print("\nCamera's state:")
        headers = ["Position (x, y, z)", "Front (x, y, z)", "Up (x, y, z)"]
        print(tabulate([self.camera_state()], headers=headers, tablefmt="grid"))
        print(
            f"\nCurrently controlling Object {i + 1} '{self.objects[i].name}'\n"
        )
