from typing import Any
from OpenGL.GL import (
    GL_FILL,
    GL_FRONT_AND_BACK,
    GL_LINE,
    GL_POLYGON_MODE,
    glGetInteger,
    glPolygonMode,
)
from glfw import (
    KEY_A as A,
    KEY_D as D,
    KEY_F as F,
    KEY_I as I,
    KEY_J as J,
    KEY_K as K,
    KEY_L as L,
    KEY_O as O,
    KEY_P as P,
    KEY_R as R,
    KEY_S as S,
    KEY_T as T,
    KEY_U as U,
    KEY_W as W,
    KEY_X as X,
    KEY_Y as Y,
    KEY_Z as Z,
    PRESS,
    get_key,
)
from objects.object import Object


class ObjectController:
    object: Object
    step: float
    window: Any

    def __init__(self, object: Object, window: Any, step: float = 0.01):
        self.object = object
        self.step = step
        self.window = window

    def handle_input(self):
        o = self.object
        w = self.window
        step = self.step

        # Position
        if get_key(w, W) == PRESS:
            o.position["z"] += step
        if get_key(w, S) == PRESS:
            o.position["z"] -= step
        if get_key(w, A) == PRESS:
            o.position["x"] -= step
        if get_key(w, D) == PRESS:
            o.position["x"] += step
        if get_key(w, R) == PRESS:
            o.position["y"] += step
        if get_key(w, F) == PRESS:
            o.position["y"] -= step

        # Scale
        if get_key(w, Z) == PRESS:
            o.scale = max(0.01, o.scale - step)
        if get_key(w, X) == PRESS:
            o.scale += step

        # Rotation
        if get_key(w, I) == PRESS:
            o.rotation["x"] += step
        if get_key(w, K) == PRESS:
            o.rotation["x"] -= step
        if get_key(w, U) == PRESS:
            o.rotation["y"] += step
        if get_key(w, O) == PRESS:
            o.rotation["y"] -= step
        if get_key(w, J) == PRESS:
            o.rotation["z"] += step
        if get_key(w, L) == PRESS:
            o.rotation["z"] -= step

        # Reset
        if get_key(w, Y) == PRESS:
            o.reset()

        # Toggle wireframe mode
        if get_key(w, P) == PRESS:
            current_mode = glGetInteger(GL_POLYGON_MODE)[0]
            if current_mode == GL_FILL:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
