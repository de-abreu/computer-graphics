# main.py

import glfw
import numpy as np
from OpenGL.GL import *

from app.window import show_window, terminate, init_window
from app.shader import create_shader_program
from app.objects.palette import Palette

VERTEX_SHADER_SOURCE = """
    attribute vec3 position;
    uniform mat4 mat_transformation;
    void main(){
        gl_Position = mat_transformation * vec4(position,1.0);
    }
"""

FRAGMENT_SHADER_SOURCE = """
    uniform vec4 color;
    void main(){
        gl_FragColor = color;
    }
"""


def main():
    # Initialize GLFW and create window
    window = init_window(720, 600, "Program")

    # Initialize shader program
    program = create_shader_program(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)

    # --- Buffer setup (for all objects) ---
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))

    # Create an instance of Ship using the foreground color from Palette
    palette = Palette()

    # Show the window and set up blending
    show_window(window)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Main loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(*palette.background, 1.0)

        # --- Input handling ---
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            ship.move(0.0, 0.01)
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            ship.move(0.0, -0.01)
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            ship.move(-0.01, 0.0)
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            ship.move(0.01, 0.0)
        if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
            ship.resize(0.99)
        if glfw.get_key(window, glfw.KEY_X) == glfw.PRESS:
            ship.resize(1.01)
        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            ship.rotate(0.02)
        if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
            ship.rotate(-0.02)
        if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
            ship.reset()
        if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
            ship.toggle_fill()

        ship.update()
        ship.draw()

        glfw.swap_buffers(window)
        glfw.poll_events()

    terminate()


if __name__ == "__main__":
    main()
