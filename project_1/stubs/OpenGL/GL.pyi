from typing import Any
from numpy.typing import NDArray
from numpy import float32

# Constants
GL_ARRAY_BUFFER: int
GL_BLEND: int
GL_COLOR_BUFFER_BIT: int
GL_DEPTH_BUFFER_BIT: int
GL_DEPTH_TEST: int
GL_DYNAMIC_DRAW: int
GL_FILL: int
GL_FLOAT: int
GL_FRONT_AND_BACK: int
GL_LINE: int
GL_ONE_MINUS_SRC_ALPHA: int
GL_POLYGON_MODE: int
GL_SRC_ALPHA: int
GL_TRIANGLES: int
GL_TRUE: int
GL_COMPILE_STATUS: int
GL_FRAGMENT_SHADER: int
GL_LINK_STATUS: int
GL_VERTEX_SHADER: int

# Functions
def glGetAttribLocation(program: int, name: str) -> int: ...
def glEnable(cap: int) -> None: ...
def glEnableVertexAttribArray(index: int) -> None: ...
def glVertexAttribPointer(
    index: int, size: int, type: int, normalized: bool, stride: int, pointer: Any
) -> None: ...
def glGetUniformLocation(program: int, name: str) -> int: ...
def glBufferData(
    target: int, size: int, data: NDArray[float32], usage: int
) -> None: ...
def glPolygonMode(face: int, mode: int) -> None: ...
def glGetInteger(pname: int) -> list[int]: ...
def glUniformMatrix4fv(
    location: int, count: int, transpose: bool | int, value: NDArray[float32]
) -> None: ...
def glUniform4f(location: int, v0: float, v1: float, v2: float, v3: float) -> None: ...
def glDrawArrays(mode: int, first: int, count: int) -> None: ...
def glBindBuffer(target: int, buffer: int) -> None: ...
def glBlendFunc(sfactor: int, dfactor: int) -> None: ...
def glClear(mask: int) -> None: ...
def glClearColor(red: float, green: float, blue: float, alpha: float) -> None: ...
def glGenBuffers(n: int) -> int: ...
def glAttachShader(program: int, shader: int) -> None: ...
def glCompileShader(shader: int) -> None: ...
def glCreateProgram() -> int: ...
def glCreateShader(shader_type: int) -> int: ...
def glGetProgramInfoLog(program: int) -> bytes: ...
def glGetProgramiv(program: int, pname: int) -> int: ...
def glGetShaderInfoLog(shader: int) -> bytes: ...
def glGetShaderiv(shader: int, pname: int) -> int: ...
def glLinkProgram(program: int) -> None: ...
def glShaderSource(shader: int, source: str) -> None: ...
def glUseProgram(program: int) -> None: ...
def compile_shader(source: str, shader_type: int) -> int: ...
def create_shader_program(vertex_source: str, fragment_source: str) -> int: ...
