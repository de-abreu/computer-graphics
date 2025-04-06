from time import sleep

from glfw import poll_events, swap_buffers, window_should_close
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
from app.logger import Logger
from app.object_controller import ObjectController
from app.objects.board import Board
from app.objects.object import Object
from app.objects.piece import Piece
from app.shader import create_shader_program
from app.window import init_window, show_window, terminate

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
    objects: list[Object] = [
        Piece(
            "pawn",
            (-0.25, -0.09, -0.17),
            (-0.47, -0.14, 0.1),
            0.07,
            palette.red,
            program,
        ),
        Piece(
            "bishop",
            (0.36, 0.01, 0.0),
            (-0.47, -0.14, 0.1),
            0.07,
            palette.magenta,
            program,
        ),
        Piece(
            "queen",
            (-0.15, 0.21, 0.0),
            (-0.47, -0.14, 0.1),
            0.07,
            palette.blue,
            program,
        ),
        Piece(
            "king",
            (-0.02, 0.04, -0.02),
            (0.29, -3.29, 0.06),
            0.07,
            palette.yellow,
            program,
        ),
        Board(
            (-0.01, 0.0, 0.05),
            (-0.67, -0.68, 0.52),
            0.7,
            [palette.white, palette.green],
            program,
        ),
    ]
    controller = ObjectController(objects, window)
    logger = Logger(objects)
    show_window(window)
    glEnable(GL_DEPTH_TEST)

    # Main loop
    while not window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*palette.background, 1.0)

        controller.handle_input()
        logger.log(controller.i)
        for obj in objects:
            obj.draw()
        sleep(1.0 / 30)  # 30 FPS target
        swap_buffers(window)
        poll_events()

    terminate()


if __name__ == "__main__":
    main()
