from .object import Object
from typing import Any
from OpenGL.GL import (
    GL_TRUE,
    GL_TRIANGLES,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glUniform4f,
    glDrawArrays,
)


class Board(Object):
    color: list[tuple[float, float, float, float]]
    _loc_color: int

    def _generate_geometry(self) -> list[tuple[float, float, float]]:
        step = 0.25
        start_x = -1.0
        start_z = -1.0
        vertices: list[tuple[float, float, float]] = []

        for row in range(8):
            for col in range(8):
                x = start_x + col * step
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
        shape = self._generate_geometry()
        super().__init__(shape, position, rotation, scale, program)
        self.color = [(r, g, b, 1.0) for r, g, b in color]
        self._loc_color = glGetUniformLocation(program, "color")

    def draw(self):
        glUniformMatrix4fv(self.loc_transformation, 1, GL_TRUE, self.transformation)
        i = 0
        for square in range(0, len(self.vertices), 6):
            # Alternate colors
            glUniform4f(self._loc_color, *self.color[i])
            glDrawArrays(GL_TRIANGLES, square, 6)
            i = (i + 1) % 2
