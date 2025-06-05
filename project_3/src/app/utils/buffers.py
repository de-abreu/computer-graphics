import ctypes
from typing import Any
from OpenGL.GL import (
    glGenBuffers,
    glBindBuffer,
    glBufferData,
    GL_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    GL_FLOAT as FLOAT,
    glGetAttribLocation,
    glEnableVertexAttribArray,
    glVertexAttribPointer,
)
from numpy import array, float32
from app.utils.dataclasses import BufferData


def init_buffers(program: Any, bd: BufferData):
    buffers = glGenBuffers(3)
    upload_data(program, buffers[0], bd.vertices, 3)
    upload_data(program, buffers[1], bd.texture_coord, 2)
    upload_data(program, buffers[2], bd.normals, 3)


def upload_data(
    program: Any,
    buffer: Any,
    coord_list: list[tuple[float, ...]],
    coord_size: int,
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
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, coord_size, FLOAT, False, stride, offset)
