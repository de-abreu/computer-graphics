from app.camera import Camera
from app.object import Object, ObjDescriptor
from app.shader import Shader
import ctypes
import os
from typing import Any
from OpenGL.raw.GL.VERSION.GL_1_0 import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_TRIANGLES as TRIANGLES,
    glClear,
    glClearColor,
    glEnable,
)
from OpenGL.raw.GL.VERSION.GL_1_1 import glDrawArrays
from OpenGL.raw.GL.VERSION.GL_1_5 import (
    GL_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    glBindBuffer,
    glBufferData,
    glGenBuffers,
)
from OpenGL.raw.GL.VERSION.GL_2_0 import (
    glEnableVertexAttribArray,
    glGetAttribLocation,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glVertexAttribPointer,
)
from OpenGL.raw.GL._types import GL_FLOAT, GL_TRUE as TRUE
from glfw import (
    get_window_size,
    set_window_user_pointer,
    show_window,
    swap_buffers,
)
from numpy import array, float32
from tabulate import tabulate


class Scene:
    camera: Camera
    program: Any
    objects: list[Object] = []
    index: int = 0

    def __init__(
        self, window: Any, obj_descriptors: list[ObjDescriptor]
    ) -> None:
        shader = Shader("src/shaders/vertex.vs", "src/shaders/fragments.fs")
        shader.use()
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
        textures = array(texture_coord, dtype=float32)
        glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride, offset = textures.strides[0], ctypes.c_void_p(0)
        loc_textures = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_textures)
        glVertexAttribPointer(loc_textures, 2, GL_FLOAT, False, stride, offset)

    def draw(self, window: Any) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0x33 / 255, 0x3C / 255, 0x43 / 255, 1.0)
        for obj in self.objects:
            mat = obj.transformation
            loc = glGetUniformLocation(self.program, "model")
            glUniformMatrix4fv(loc, 1, TRUE, mat)
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
        cam = self.camera
        state: list[str] = [
            f"({cam.pos.x:.2f}, {cam.pos.y:.2f}, {cam.pos.z:.2f})",
            f"({cam.front.x:.2f}, {cam.front.y:.2f}, {cam.front.z:.2f})",
            f"({cam.up.x:.2f}, {cam.up.y:.2f}, {cam.up.z:.2f})",
        ]
        return state

    def log(self) -> None:
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
        headers = ["Position", "Front", "Up"]
        print(tabulate([self.camera_state()], headers=headers, tablefmt="grid"))
        print(
            f"\nCurrently controlling Object {i + 1} '{self.objects[i].name}'\n"
        )
