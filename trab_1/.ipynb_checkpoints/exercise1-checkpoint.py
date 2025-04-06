# INFO: Initial setup, as per the original notebook

import math

import glfw
import glm
import numpy as np
from OpenGL.GL import *
from numpy.typing import NDArray
from dataclasses import dataclass, field

# Window initialization

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 600, "Programa", None, None)

if window is None:
    print("Failed to create GLFW window")
    glfw.terminate()

glfw.make_context_current(window)

# Shaders

vertex_code = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
        """

fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

# Requesting a GPU slot for the shaders
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Assigning our source code to the shaders
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compiling the Vertex shader
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

# Compiling the Fragment shader
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# Associating shaders to the main program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError("Linking error")

# Make program the default program
glUseProgram(program)

# --- Buffer Setup ---
buffer_VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO)

# INFO: Original code starts here


@dataclass
class Pallete:  # Ayu mirage color pallete
    foreground: tuple[float, float, float] = field(
        default_factory=lambda: (0xFF / 255, 0xAD / 255, 0x66 / 255)
    )
    background: tuple[float, float, float] = field(
        default_factory=lambda: (0x24 / 255, 0x29 / 255, 0x36 / 255)
    )


class ship:
    def __init__(self, size: float, color: tuple[float, float, float]):
        self.initial_size = size
        self.vertices = np.array(
            [
                (0.0, size),  # Top point
                (-size * math.sqrt(3) / 2, -size / 2),  # Bottom left
                (size * math.sqrt(3) / 2, -size / 2),  # Bottom right
            ],
            dtype=np.float32,
        )
        self.reset()

        # --- Attribute and Uniform Setup ---
        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)

        self.loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(self.loc)
        glVertexAttribPointer(self.loc, 2, GL_FLOAT, False, stride, offset)

        self.loc_color = glGetUniformLocation(program, "color")
        self.color = color + (1.0,)
        self.loc_transformation = glGetUniformLocation(program, "mat_transformation")

        # Send initial vertices to GPU once
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW
        )

    def update(self):
        s = self.scale
        scale = np.array(
            [
                [s, 0.0, 0.0, 0.0],
                [0.0, s, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

        cos = np.cos(self.rotation)
        sin = np.sin(self.rotation)
        rotate = np.array(
            [
                [cos, -sin, 0.0, 0.0],
                [sin, cos, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

        p = self.position
        translate = np.array(
            [
                [1.0, 0.0, 0.0, p[0]],
                [0.0, 1.0, 0.0, p[1]],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

        # Applying transformation to vertices
        self.transformation = (translate @ rotate @ scale).T

    def move(self, x_offset: float, y_offset: float):
        self.position[0] += x_offset
        self.position[1] += y_offset

    def resize(self, scale_factor: float):
        self.scale *= scale_factor

    def rotate(self, angle: float):
        self.rotation += angle

    def reset(self):
        self.position = np.array([0.0, 0.0], dtype=np.float32)
        self.scale = 1.0
        self.rotation = 0.0
        self.update()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def toggle_fill(self):
        current_mode = glGetInteger(GL_POLYGON_MODE)[0]
        if current_mode == GL_FILL:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw(self):
        # Upload the transformation matrix
        glUniformMatrix4fv(self.loc_transformation, 1, GL_FALSE, self.transformation)

        # Set color
        glUniform4f(self.loc_color, *self.color)

        # Draw shape
        glDrawArrays(GL_TRIANGLES, 0, 3)


# --- Creating ship instance ---
s = ship(0.2, Pallete().foreground)

# --- Window Display and Blending ---
glfw.show_window(window)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# --- Main Loop ---
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(*Pallete().background, 1.0)

    # --- Input handling ---
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        s.move(0.0, 0.01)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        s.move(0.0, -0.01)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        s.move(-0.01, 0.0)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        s.move(0.01, 0.0)
    if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
        s.resize(0.99)
    if glfw.get_key(window, glfw.KEY_X) == glfw.PRESS:
        s.resize(1.01)
    if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
        s.rotate(0.02)
    if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
        s.rotate(-0.02)
    if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
        s.reset()
    if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
        s.toggle_fill()

    s.update()
    s.draw()
    glfw.swap_buffers(window)
    glfw.poll_events()
glfw.terminate()
