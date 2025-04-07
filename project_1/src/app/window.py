from typing import Any
import glfw


def show_window(window: Any) -> None:
    glfw.show_window(window)


def terminate():
    glfw.terminate()


def init_window(width: int, height: int, title: str):
    if not glfw.init():
        raise Exception("GLFW initialization failed")
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(width, height, title, None, None)
    if window is None:
        terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)
    return window
