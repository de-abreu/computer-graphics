from typing import Any
from glfw import (
    FALSE,
    VISIBLE,
    create_window,
    init,
    make_context_current,
    terminate,
    window_hint,
)


def init_window(width: int, height: int, title: str) -> Any:
    if not init():
        raise Exception("GLFW initialization failed")
    window_hint(VISIBLE, FALSE)
    window = create_window(width, height, title, None, None)
    if window is None:
        terminate()
        raise RuntimeError("Failed to create GLFW window")

    make_context_current(window)
    return window
