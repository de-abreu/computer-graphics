from .object import Object
from typing import Any, override
from OpenGL.GL import (
    GL_TRUE,
    GL_TRIANGLES,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glUniform4f,
    glDrawArrays,
)


class Board(Object):
    """
    A class representing a chessboard, inheriting from the Object class.

    Attributes:
        color (list[tuple[float, float, float, float]]): A list of RGBA colors for the squares on the board.
        _loc_color (int): The location of the color uniform in the shader program.
    """

    color: list[tuple[float, float, float, float]]
    _loc_color: int

    @staticmethod
    def _generate_geometry() -> list[tuple[float, float, float]]:
        """
        Generates the geometry for the chessboard.

        This method creates the vertex data for the squares of the chessboard,
        defining the corners of each square and returning a list of vertices.

        Returns:
            list[tuple[float, float, float]]: A list of vertices representing the geometry of the chessboard.
        """
        step = 0.25
        start_x = -1.0
        start_z = -1.0
        vertices: list[tuple[float, float, float]] = []

        for row in range(8):
            for col in range(8):
                x = start_x + row * step
                z = start_z + col * step

                # The four corners of a given square
                p = [
                    (x, 0.0, z),
                    (x, 0.0, z + step),
                    (x + step, 0.0, z),
                    (x + step, 0.0, z + step),
                ]

                # Bottom-left triangle portion of the square
                vertices.extend(p[:3])

                # Top-right triangle portion of the square
                vertices.extend(p[1:])
        return vertices

    def __init__(
        self,
        position: tuple[float, float, float],
        rotation: tuple[float, float, float],
        scale: float,
        color: list[tuple[float, float, float]],
        program: Any,
    ):
        """
        Initializes the Board with its position, rotation, scale, colors, and shader program.

        Args:
            position (tuple[float, float, float]): The initial position of the board in 3D space.
            rotation (tuple[float, float, float]): The initial rotation of the board in degrees around the x, y, and z axes.
            scale (float): The scale factor for the board.
            color (list[tuple[float, float, float]]): A list of RGB colors for the squares on the board.
            program (Any): The shader program used for rendering the board.
        """
        shape = self._generate_geometry()
        super().__init__(shape, position, rotation, scale, program)
        self.color = [(r, g, b, 1.0) for r, g, b in color]
        self._loc_color = glGetUniformLocation(program, "color")

    @override
    def draw(self):
        """
        Prepares the board for rendering by setting up the necessary OpenGL state.

        This method calls the parent class's draw method to handle the basic drawing setup,
        then sets the transformation matrix and color uniform for each square. It iterates over
        the vertices of the board and issues draw calls to render the squares in alternating colors.

        This method should be called within the rendering loop to display the board on the screen.
        """
        super().draw()
        glUniformMatrix4fv(self.loc_transformation, 1, GL_TRUE, self.transformation)
        i = 0
        for square in range(0, len(self.vertices), 6):
            row = i // 8  # Integer division to get the row
            col = i % 8  # Modulus to get the column
            j = (row + col) % 2  # 0 or 1 for alternating colors

            glUniform4f(self._loc_color, *self.color[j])
            glDrawArrays(GL_TRIANGLES, square, 6)
            i += 1
