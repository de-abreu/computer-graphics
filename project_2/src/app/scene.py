# pyright: reportCallIssue=false
from app.camera import Camera
from app.object import Object, ObjDescriptor
from app.shader import Shader
import ctypes
import os
from typing import Any
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_BLEND,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_DONT_CARE,
    GL_FLOAT,
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
    glUniformMatrix4fv,
    glVertexAttribPointer,
)
from glfw import (
    get_window_size,
    set_window_user_pointer,
    show_window,
    swap_buffers,
)
from numpy import array, float32
from tabulate import tabulate


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

    def __init__(
        self, window: Any, obj_descriptors: list[ObjDescriptor]
    ) -> None:
        shader = Shader("src/shaders/vertex.vs", "src/shaders/fragments.fs")
        shader.use()
        glEnable(GL_TEXTURE_2D)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        width, height = get_window_size(window)
        vertices_list: list[tuple[float, float, float]] = []
        texture_coord: list[tuple[float, float]] = []
        self.camera = Camera(width, height)
        self.program = shader.getProgram()
        for i in range(len(obj_descriptors)):
            self.objects.append(
                Object(
                    i,
                    obj_descriptors[i],
                    vertices_list,
                    texture_coord,
                )
            )

        buffers = glGenBuffers(2)
        self._upload_vertices(vertices_list, buffers)
        self._upload_textures(texture_coord, buffers)
        set_window_user_pointer(window, self)
        show_window(window)
        glEnable(GL_DEPTH_TEST)

    def _upload_vertices(
        self, vertices_list: list[tuple[float, float, float]], buffer: Any
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
        vertices = array(vertices_list, dtype=float32)
        glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride, offset = vertices.strides[0], ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

    def _upload_textures(
        self, texture_coord: list[tuple[float, float]], buffer: Any
    ) -> None:
        """
        Upload texture coordinates to the GPU.

        Parameters
        ----------
        texture_coord : list[tuple[float, float]]
            List of texture coordinates (u, v).
        buffer : Any
            The OpenGL buffer ID for texture data.
        """
        textures = array(texture_coord, dtype=float32)
        glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride, offset = textures.strides[0], ctypes.c_void_p(0)
        loc_textures = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_textures)
        glVertexAttribPointer(loc_textures, 2, GL_FLOAT, False, stride, offset)

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
