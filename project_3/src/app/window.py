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
    """
    Initialize a GLFW window with the specified dimensions and title.

    Parameters
    ----------
    width : int
        The width of the window in pixels.
    height : int
        The height of the window in pixels.
    title : str
        The title to display in the window's title bar.

    Returns
    -------
    Any
        The GLFW window object.

    Raises
    ------
    Exception
        If GLFW initialization fails.
    RuntimeError
        If window creation fails.

    Notes
    -----
    This function:
    1. Initializes GLFW
    2. Creates an invisible window (initially hidden)
    3. Sets the window's OpenGL context as current
    4. Returns the window handle for further operations
    """
    if not init():
        raise Exception("GLFW initialization failed")
    window_hint(VISIBLE, FALSE)
    window = create_window(width, height, title, None, None)
    if window is None:
        terminate()
        raise RuntimeError("Failed to create GLFW window")

    make_context_current(window)
    return window
