from .object import Object
from math import tau, cos, sin
from .silhouettes.bishop import BISHOP_SILHOUETTE
from .silhouettes.king import KING_SILHOUETTE, KING_CROWN
from .silhouettes.pawn import PAWN_SILHOUETTE
from .silhouettes.queen import QUEEN_SILHOUETTE
from typing import Any, override
from OpenGL.GL import (
    GL_TRUE,
    GL_TRIANGLES,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glUniform4f,
    glDrawArrays,
)


class Piece(Object):
    color: tuple[float, float, float, float]
    _loc_color: int

    # Trigonometric formula to return the coordinate of a vertex at the edge of
    # a cylinder
    @staticmethod
    def _vert_coordinate(
        angle: float, height: float, radius: float
    ) -> tuple[float, float, float]:
        return (radius * cos(angle), height, radius * sin(angle))  # (x, y, z)

    # Function to place vertices at the edges of a type's given shape
    def _set_vertices(
        self, silhouette: list[tuple[float, float]], sectors: int
    ) -> list[tuple[float, float, float]]:
        step = tau / sectors
        coordinate = self._vert_coordinate
        radii, heights = [list(t) for t in zip(*silhouette)]
        vertices: list[tuple[float, float, float]] = []

        # type's bottom
        for s in range(sectors):
            angle = s * step
            next_angle = (s + 1) % sectors * step
            vertices.append(coordinate(angle, heights[0], radii[0]))
            vertices.append(coordinate(next_angle, heights[0], radii[0]))
            vertices.append((0.0, 0.0, 0.0))

        # type's side
        for h in range(len(heights) - 1):
            next_h = h + 1
            for s in range(sectors):
                angle = s * step
                next_angle = (s + 1) % sectors * step

                # Square shaped face
                p = [
                    coordinate(angle, heights[h], radii[h]),
                    coordinate(angle, heights[next_h], radii[next_h]),
                    coordinate(next_angle, heights[h], radii[h]),
                    coordinate(next_angle, heights[next_h], radii[next_h]),
                ]

                # Bottom-left triangle portion of the square
                vertices.extend(p[:3])

                # Top-right triangle portion of the square
                vertices.extend(p[1:])

        # type's top
        for s in range(sectors):
            angle = s * step
            next_angle = (s + 1) % sectors * step
            vertices.append(coordinate(angle, heights[-1], radii[-1]))
            vertices.append(coordinate(next_angle, heights[-1], radii[-1]))
            vertices.append((0.0, heights[-1], 0.0))

        return vertices

    def __init__(
        self,
        type: str,
        position: tuple[float, float, float],
        rotation: tuple[float, float, float],
        scale: float,
        color: tuple[float, float, float],
        program: Any,
    ):
        sectors = 8
        # Coordinates of the type's silhouette, given in (radius, height). The base
        # is the same for all varieties of types.
        base_silhouette = [(0.6, 0.0), (0.8, 0.2), (0.6, 0.8), (0.4, 1.0)]
        set_vertices = self._set_vertices

        match type:
            case "pawn":
                shape = set_vertices(base_silhouette + PAWN_SILHOUETTE, sectors)
            case "bishop":
                shape = set_vertices(base_silhouette + BISHOP_SILHOUETTE, sectors)
            case "queen":
                shape = set_vertices(base_silhouette + QUEEN_SILHOUETTE, sectors)
            case _:
                shape = set_vertices(base_silhouette + KING_SILHOUETTE, sectors)
                shape += KING_CROWN

        super().__init__(shape, position, rotation, scale, program)
        self.color = color + (1.0,)
        self._loc_color = glGetUniformLocation(program, "color")

    @override
    def draw(self):
        super().draw()
        glUniformMatrix4fv(self.loc, 1, GL_TRUE, self.transformation)
        glUniform4f(self._loc_color, *self.color)
        for triangle in range(0, len(self.vertices), 3):
            glDrawArrays(GL_TRIANGLES, triangle, 3)
