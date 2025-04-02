from math import tau, cos, sin
from objects.piece import Piece
from silhouettes.bishop import BISHOP_SILHOUETTE
from silhouettes.pawn import PAWN_SILHOUETTE
from silhouettes.KING import KING_SILHOUETTE, KING_CROWN
from silhouettes.queen import QUEEN_SILHOUETTE


def piece_factory(type: str, color: tuple[float, float, float]) -> Piece:
    sectors = 8
    # Coordinates of the piece's silhouette, given in (radius, height). The base
    # is the same for all varieties of pieces.
    silhouette = [(0.6, 0.0), (0.8, 0.2), (0.6, 0.8), (0.4, 1.0)]

    # Trigonometric formula to return a point at the edge of a cylinder
    def VertCoordinate(
        angle: float, height: float, radius: float
    ) -> tuple[float, float, float]:
        return (radius * cos(angle), radius * sin(angle), height)  # (x, y, z)

    # Function to place vertices at the edges of a piece's given shape
    def SetVertices(
        silhouette: list[tuple[float, float]], sectors: int
    ) -> list[tuple[float, float, float]]:
        step = tau / sectors
        radii, heights = [list(t) for t in zip(*silhouette)]
        vertices = []

        # Piece's bottom
        for i in range(sectors):
            j = (i + 1) % sectors
            vertices.append(VertCoordinate(i * step, heights[0], radii[0]))
            vertices.append(VertCoordinate(j * step, heights[0], radii[0]))
            vertices.append((0.0, 0.0, 0.0))

        # Piece's side
        for k in range(len(silhouette) - 1):
            for i in range(sectors):
                j = i + 1
                angle = i * step
                angle_next = j * step

                # Square shaped face
                p = [
                    VertCoordinate(angle, heights[i], radii[i]),
                    VertCoordinate(angle, heights[j], radii[j]),
                    VertCoordinate(angle_next, heights[i], radii[i]),
                    VertCoordinate(angle_next, heights[j], radii[j]),
                ]

                # Bottom-left triangle portion of the square
                vertices.append(p[:3])

                # Top-right triangle portion of the square
                vertices.append(p[1:])

        # Piece's top
        for i in range(sectors):
            j = (i + 1) % sectors
            vertices.append(VertCoordinate(i * step, heights[-1], radii[-1]))
            vertices.append(VertCoordinate(j * step, heights[-1], radii[-1]))
            vertices.append((0.0, heights[-1], 0.0))

        return vertices

    match type:
        case "pawn":
            silhouette += PAWN_SILHOUETTE
            return Piece(SetVertices(silhouette, sectors), color)
        case "bishop":
            silhouette += BISHOP_SILHOUETTE
            return Piece(SetVertices(silhouette, sectors), color)
        case "queen":
            silhouette += QUEEN_SILHOUETTE
            return Piece(SetVertices(silhouette, sectors), color)
        case _:
            silhouette += KING_SILHOUETTE
            return Piece(SetVertices(silhouette + KING_CROWN, sectors), color)
