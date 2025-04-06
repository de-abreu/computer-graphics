from time import sleep
from glfw import window_should_close, swap_buffers, poll_events
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
from app.color_pallete import Palette
from app.objects.board import Board
from app.objects.piece import Piece
from app.shader import create_shader_program
from app.window import show_window, terminate, init_window
from app.object_controller import ObjectController

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
    window = init_window(940, 1000, "Program")
    program = create_shader_program(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    palette = Palette()
    objects = [
        Piece("pawn", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.15, palette.red, program),
        Piece(
            "bishop", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.15, palette.magenta, program
        ),
        Piece("queen", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.15, palette.blue, program),
        Piece("king", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.15, palette.yellow, program),
        Board(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            1.0,
            [palette.white, palette.green],
            program,
        ),
    ]
    controller = ObjectController(objects, window)
    show_window(window)
    glEnable(GL_DEPTH_TEST)

    # Main loop
    while not window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*palette.background, 1.0)

        controller.handle_input()
        for obj in objects:
            obj.draw()
        sleep(1.0 / 30)  # 30 FPS target
        swap_buffers(window)
        poll_events()

    terminate()


if __name__ == "__main__":
    main()
