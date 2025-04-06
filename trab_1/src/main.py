import glfw
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    glBindBuffer,
    glClear,
    glClearColor,
    glEnable,
    glGenBuffers,
)
from app.window import show_window, terminate, init_window
from app.shader import create_shader_program
from app.color_pallete import Palette
from app.object_controller import ObjectController
from app.objects.piece import Piece

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
    window = init_window(720, 600, "Program")
    program = create_shader_program(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    palette = Palette()
    pawn = Piece(
        "pawn", (0.0, 0.0, -3.0), (0.0, 0.0, 0.0), 0.25, palette.yellow, program
    )
    controller = ObjectController(pawn, window)
    show_window(window)
    glEnable(GL_DEPTH_TEST)

    # Main loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*palette.background, 1.0)

        controller.handle_input()
        pawn.draw()
        glfw.swap_buffers(window)
        glfw.poll_events()

    terminate()


if __name__ == "__main__":
    main()
