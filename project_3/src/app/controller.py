import os
from app.scene import Scene
from app.utils import Mode
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
    KEY_1,
    KEY_2,
    KEY_3,
    KEY_4,
    KEY_5,
    KEY_A as A,
    KEY_D as D,
    KEY_E as E,
    KEY_ESCAPE as ESC,
    KEY_Q as Q,
    KEY_R as R,
    KEY_S as S,
    KEY_T as T,
    KEY_W as W,
    KEY_X as X,
    KEY_Z as Z,
    PRESS,
    RAW_MOUSE_MOTION,
    REPEAT,
    TRUE,
    get_window_user_pointer,
    raw_mouse_motion_supported,
    set_cursor_pos_callback,
    set_framebuffer_size_callback,
    set_input_mode,
    set_key_callback,
    set_scroll_callback,
    set_window_should_close,
    set_window_user_pointer,
)
from tabulate import tabulate


class Controller:
    """Handles user input and controls the scene's objects, camera, and lights.

    Attributes
    ----------
    current_object : int
        Index of the currently selected object in the scene.
    mode : Mode
        Current interaction mode (e.g., camera, translating, rotating, scaling, light).
    scene : Scene
        The scene being controlled.
    """

    current_object: int = 0
    mode: Mode = Mode.camera
    scene: Scene

    def __init__(self, scene: Scene) -> None:
        """Initialize the Controller with a scene and set up input callbacks.

        Parameters
        ----------
        scene : Scene
            The scene to be controlled.
        """
        self.scene = scene
        win = scene.window
        set_window_user_pointer(win, self)
        set_input_mode(win, CURSOR, CURSOR_DISABLED)
        if raw_mouse_motion_supported():
            set_input_mode(win, RAW_MOUSE_MOTION, TRUE)

        set_key_callback(win, self._keyboard_callback)
        set_framebuffer_size_callback(win, self._framebuffer_callback)
        set_cursor_pos_callback(win, self._mouse_callback)
        set_scroll_callback(win, self._scroll_callback)

    @staticmethod
    def _keyboard_callback(
        window: Any, key: int, _scancode: int, action: int, _mods: int
    ):
        ctrl: Controller = get_window_user_pointer(window)
        i = ctrl.current_object
        scene = ctrl.scene
        o = scene.objects[i]
        c = scene.camera
        step = 0.1

        # INFO: WASD and QE keys set to manipulate objects or camera
        if key == W and action in (PRESS, REPEAT):
            match ctrl.mode:
                case Mode.camera:
                    _ = c.move(step * 2, "z")
                case Mode.rotating:
                    o.rotation["x"] -= step
                case Mode.translating:
                    o.position["z"] -= step
                case Mode.scaling:
                    o.scale += step
                case _:
                    scene.ambient_light_on = not scene.ambient_light_on

        if key == S and action in (PRESS, REPEAT):
            match ctrl.mode:
                case Mode.camera:
                    _ = c.move(-step * 2, "z")
                case Mode.rotating:
                    o.rotation["x"] += step
                case Mode.translating:
                    o.position["z"] += step
                case Mode.scaling:
                    o.scale -= step
                case _:
                    _ = scene.light_sources[1].toggle()

        if key == A and action in (PRESS, REPEAT):
            match ctrl.mode:
                case Mode.camera:
                    _ = c.move(-step * 2, "x")
                case Mode.rotating:
                    o.rotation["y"] -= step
                case Mode.translating:
                    o.position["x"] -= step
                case Mode.light:
                    _ = scene.light_sources[0].toggle()
                case _:
                    pass

        if key == D and action in (PRESS, REPEAT):
            match ctrl.mode:
                case Mode.camera:
                    _ = c.move(step * 2, "x")
                case Mode.rotating:
                    o.rotation["y"] += step
                case Mode.translating:
                    o.position["x"] += step
                case Mode.light:
                    _ = scene.light_sources[2].toggle()
                case _:
                    pass

        if key == Q and action in (PRESS, REPEAT):
            match ctrl.mode:
                case Mode.camera:
                    _ = c.move(step * 2, "y")
                case Mode.rotating:
                    o.rotation["z"] += step
                case Mode.translating:
                    o.position["y"] += step
                case _:
                    pass

        if key == E and action in (PRESS, REPEAT):
            match ctrl.mode:
                case Mode.camera:
                    _ = c.move(-step * 2, "y")
                case Mode.rotating:
                    o.rotation["z"] -= step
                case Mode.translating:
                    o.position["y"] -= step
                case _:
                    pass

        if key == KEY_1 and action == PRESS:
            ctrl.mode = Mode.camera

        if key == KEY_2 and action == PRESS:
            ctrl.mode = Mode.translating

        if key == KEY_3 and action == PRESS:
            ctrl.mode = Mode.rotating

        if key == KEY_4 and action == PRESS:
            ctrl.mode = Mode.scaling

        if key == KEY_5 and action == PRESS:
            ctrl.mode = Mode.light

        if key == T and action == PRESS:
            current_mode = glGetInteger(GL_POLYGON_MODE)[0]
            if current_mode == GL_FILL:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if key == R and action == PRESS:
            _ = o.reset()

        if key == ESC and action == PRESS:
            set_window_should_close(window, True)

        if key == Z and action in (PRESS, REPEAT):
            ctrl.current_object = (i - 1) % len(scene.objects)

        if key == X and action in (PRESS, REPEAT):
            ctrl.current_object = (i + 1) % len(scene.objects)

    @staticmethod
    def _framebuffer_callback(_window: Any, width: int, height: int) -> None:
        glViewport(0, 0, width, height)

    @staticmethod
    def _mouse_callback(window: Any, x_pos: float, y_pos: float) -> None:
        ctrl: Controller = get_window_user_pointer(window)
        c = ctrl.scene.camera

        if c.first_mouse:
            c.last_x = x_pos
            c.last_y = y_pos
            c.first_mouse = False

        x_offset = x_pos - c.last_x
        # The following is reversed since y-coordinates go from bottom to top
        y_offset = c.last_y - y_pos
        c.last_x = x_pos
        c.last_y = y_pos
        _ = c.process_mouse_movement(x_offset, y_offset)

    @staticmethod
    def _scroll_callback(
        window: Any, _x_offset: float, y_offset: float
    ) -> None:
        ctrl: Controller = get_window_user_pointer(window)
        _ = ctrl.scene.camera.process_scroll_movement(y_offset)

    def _objects_state(self) -> list[list[str]]:
        state: list[list[str]] = []
        for i, obj in enumerate(self.scene.objects):
            state.append(
                [
                    f"{i + 1}",
                    f"({obj.position['x']:.2f}, {obj.position['y']:.2f}, {obj.position['z']:.2f})",
                    f"({obj.rotation['x']:.2f}, {obj.rotation['y']:.2f}, {obj.rotation['z']:.2f})",
                    f"{obj.scale:.2f}",
                ]
            )
        return state

    def _camera_state(self) -> list[str]:
        cam = self.scene.camera
        return [
            f"({cam.pos.x:.2f}, {cam.pos.y:.2f}, {cam.pos.z:.2f})",
            f"({cam.front.x:.2f}, {cam.front.y:.2f}, {cam.front.z:.2f})",
            f"({cam.up.x:.2f}, {cam.up.y:.2f}, {cam.up.z:.2f})",
        ]

    def _lights_state(self) -> list[str]:
        scene = self.scene
        state = ["On" if scene.ambient_light_on else "Off"]
        for light in scene.light_sources:
            state.append("On" if light.on else "Off")
        return state

    def log(self) -> None:
        """Print the current state of objects, camera, and lights to the console.

        Notes
        -----
        - Uses `tabulate` with `tablefmt="simple"` for aligned output without borders.
        - Clears the console before printing for better readability.
        - Displays:
            - Objects' positions, rotations, and scales.
            - Camera's position, front, and up vectors.
            - Lights' on/off states.
            - Currently controlled object and interaction mode.
        """
        i = self.current_object
        scene = self.scene
        o = scene.objects
        light = scene.light_sources
        _ = os.system("clear")

        print("Objects' state:")
        headers = [
            "Object",
            "Position (x, y, z)",
            "Rotation (x, y, z)",
            "Scale",
        ]
        print(tabulate(self._objects_state(), headers=headers))

        print("\nCamera's state:")
        headers = ["Position (x, y, z)", "Front (x, y, z)", "Up (x, y, z)"]
        print(tabulate([self._camera_state()], headers=headers))

        print("\nLights' state:")
        headers = ["Ambient"] + [f"Light {i}" for i in range(len(light))]
        print(tabulate([self._lights_state()], headers=headers))

        title = f"\nCurrently controlling Object {i + 1} '{o[i].name}'. Mode: "
        match self.mode:
            case Mode.camera:
                print(title + "CAMERA\n")
            case Mode.rotating:
                print(title + "ROTATE\n")
            case Mode.translating:
                print(title + "MOVE\n")
            case Mode.scaling:
                print(title + "SCALE\n")
            case _:
                print(title + "LIGHT\n")
