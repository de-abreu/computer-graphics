from app.scene import Scene
from typing import Any
from OpenGL.GL import (
    GL_FILL,
    GL_FRONT_AND_BACK,
    GL_LINE,
    GL_POLYGON_MODE,
    glGetInteger,
    glPolygonMode,
    glViewport,
)
from glfw import (
    CURSOR,
    CURSOR_DISABLED,
    KEY_0,
    KEY_1,
    KEY_2,
    KEY_3,
    KEY_4,
    KEY_5,
    KEY_6,
    KEY_7,
    KEY_8,
    KEY_9,
    KEY_A as A,
    KEY_B as B,
    KEY_C as C,
    KEY_D as D,
    KEY_E as E,
    KEY_F as F,
    KEY_G as G,
    KEY_H as H,
    KEY_I as I,
    KEY_J as J,
    KEY_K as K,
    KEY_L as L,
    KEY_O as O,
    KEY_P as P,
    KEY_Q as Q,
    KEY_R as R,
    KEY_S as S,
    KEY_T as T,
    KEY_U as U,
    KEY_V as V,
    KEY_W as W,
    KEY_X as X,
    KEY_Y as Y,
    KEY_Z as Z,
    KEY_ESCAPE as ESC,
    PRESS,
    REPEAT,
    RAW_MOUSE_MOTION,
    TRUE,
    get_window_user_pointer,
    raw_mouse_motion_supported,
    set_cursor_pos_callback,
    set_framebuffer_size_callback,
    set_input_mode,
    set_key_callback,
    set_scroll_callback,
    set_window_should_close,
)


def keyboard_callback(
    window: Any, key: int, _scancode: int, action: int, _mods: int
):
    """
    Handle keyboard input for controlling the scene and objects.

    Parameters
    ----------
    window : Any
        The GLFW window object.
    key : int
        The key that was pressed or released.
    _scancode : int
        The system-specific scancode of the key.
    action : int
        The action (PRESS, REPEAT, or RELEASE).
    _mods : int
        Bit field describing which modifier keys were held down.

    Notes
    -----
    This function maps keyboard inputs to camera and object transformations.
    """
    scene: Scene = get_window_user_pointer(window)
    i = scene.index
    o = scene.objects[i]
    c = scene.camera
    step = 0.1

    # INFO: Camera position

    # Move forwards and backwards
    if key == W and action in (PRESS, REPEAT):
        _ = c.move(step * 2, "z")
    if key == S and action in (PRESS, REPEAT):
        _ = c.move(-step * 2, "z")

    # Pan
    if key == A and action in (PRESS, REPEAT):
        _ = c.move(-step * 2, "x")
    if key == D and action in (PRESS, REPEAT):
        _ = c.move(step * 2, "x")

    # Tilt
    if key == Q and action in (PRESS, REPEAT):
        _ = c.move(step * 2, "y")
    if key == E and action in (PRESS, REPEAT):
        _ = c.move(-step * 2, "y")

    # INFO: Object selection controls

    for i, keynum in enumerate(
        [KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9, KEY_0]
    ):
        if key == keynum and action == PRESS:
            scene.index = i % len(scene.objects)

    # Switch object being controlled
    if key == Z and action == PRESS:
        scene.index = (scene.index - 1) % len(scene.objects)
    if key == X and action == PRESS:
        scene.index = (scene.index + 1) % len(scene.objects)

    # INFO: Selected object controls

    # Move away/closer
    if key == T and action in (PRESS, REPEAT):
        o.position["z"] -= step
    if key == G and action in (PRESS, REPEAT):
        o.position["z"] += step

    # Move horizontally
    if key == F and action in (PRESS, REPEAT):
        o.position["x"] -= step
    if key == H and action in (PRESS, REPEAT):
        o.position["x"] += step

    # Move vertically
    if key == R and action in (PRESS, REPEAT):
        o.position["y"] += step
    if key == Y and action in (PRESS, REPEAT):
        o.position["y"] -= step

    # Roll
    if key == U and action in (PRESS, REPEAT):
        o.rotation["z"] += step
    if key == O and action in (PRESS, REPEAT):
        o.rotation["z"] -= step

    # Pitch
    if key == I and action in (PRESS, REPEAT):
        o.rotation["x"] -= step
    if key == K and action in (PRESS, REPEAT):
        o.rotation["x"] += step

    # Yaw
    if key == L and action in (PRESS, REPEAT):
        o.rotation["y"] += step
    if key == J and action in (PRESS, REPEAT):
        o.rotation["y"] -= step

    # Scale
    if key == C and action in (PRESS, REPEAT):
        o.scale -= step
    if key == V and action in (PRESS, REPEAT):
        o.scale += step

    # Toggle wireframe mode
    if key == P and action == PRESS:
        current_mode = glGetInteger(GL_POLYGON_MODE)[0]
        if current_mode == GL_FILL:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Reset object
    if key == B and action == PRESS:
        _ = o.reset()

    # Close window
    if key == ESC and action == PRESS:
        set_window_should_close(window, True)


def framebuffer_callback(_window: Any, width: int, height: int) -> None:
    """
    Handle framebuffer size changes.

    Parameters
    ----------
    _window : Any
        The GLFW window object (unused).
    width : int
        The new width of the framebuffer.
    height : int
        The new height of the framebuffer.

    Notes
    -----
    Updates the viewport to match the new framebuffer dimensions.
    """
    glViewport(0, 0, width, height)


def mouse_callback(window: Any, x_pos: float, y_pos: float) -> None:
    """
    Handle mouse movement for camera rotation.

    Parameters
    ----------
    window : Any
        The GLFW window object.
    x_pos : float
        The current x-coordinate of the mouse cursor.
    y_pos : float
        The current y-coordinate of the mouse cursor.
    """
    scene: Scene = get_window_user_pointer(window)
    camera = scene.camera

    if camera.first_mouse:
        camera.last_x = x_pos
        camera.last_y = y_pos
        camera.first_mouse = False

    x_offset = x_pos - camera.last_x
    # The following is reversed since y-coordinates go from bottom to top
    y_offset = camera.last_y - y_pos
    camera.last_x = x_pos
    camera.last_y = y_pos
    _ = camera.process_mouse_movement(x_offset, y_offset)


def scroll_callback(window: Any, _x_offset: float, y_offset: float) -> None:
    """
    Handle mouse scroll for camera zoom.

    Parameters
    ----------
    window : Any
        The GLFW window object.
    _x_offset : float
        The horizontal scroll offset (unused).
    y_offset : float
        The vertical scroll offset.
    """
    scene: Scene = get_window_user_pointer(window)
    _ = scene.camera.process_scroll_movement(y_offset)


def init_controller(window: Any):
    """
    Initialize the controller by setting up input callbacks.

    Parameters
    ----------
    window : Any
        The GLFW window object.

    Note
    ----
    For more information on how to setup the input mode and its callbacks, see: https://www.glfw.org/docs/3.3/input_guide.html
    """
    set_input_mode(window, CURSOR, CURSOR_DISABLED)
    if raw_mouse_motion_supported():
        set_input_mode(window, RAW_MOUSE_MOTION, TRUE)

    set_key_callback(window, keyboard_callback)
    set_framebuffer_size_callback(window, framebuffer_callback)
    set_cursor_pos_callback(window, mouse_callback)
    set_scroll_callback(window, scroll_callback)
