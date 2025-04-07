from typing import Any
import glfw


def show_window(window: Any) -> None:
    """
    Makes the specified GLFW window visible.

    This function makes the window visible, but does not bring it to the front.
    If the window is already visible or is in full screen mode, this function does nothing.

    Args:
        window (Any): The GLFW window handle to be shown.

    Note:
        This function must only be called from the main thread.
    """
    glfw.show_window(window)


def terminate() -> None:
    """
    Terminates the GLFW library.

    This function destroys all remaining windows and cursors, restores any modified gamma ramps,
    and frees any other allocated resources. Once this function is called, you must again call
    `glfw.init` successfully before you will be able to use most GLFW functions.

    If GLFW has been successfully initialized, this function should be called before the application exits.
    If initialization fails, there is no need to call this function, as it is called by `glfw.init` automatically.

    Note:
        This function must only be called from the main thread.
    """
    glfw.terminate()


def init_window(width: int, height: int, title: str) -> Any:
    """
    Initializes GLFW and creates a window with the specified width, height, and title.

    This function initializes the GLFW library, sets the window hints, creates a window,
    and makes the window's context current.

    Args:
        width (int): The desired width, in screen coordinates, of the window.
        height (int): The desired height, in screen coordinates, of the window.
        title (str): The initial, UTF-8 encoded title of the window.

    Returns:
        Any: The handle of the created window, or `None` if an error occurred.

    Raises:
        Exception: If GLFW initialization fails.
        RuntimeError: If the window creation fails.

    Note:
        This function must only be called from the main thread.
        The created window is initially not visible. Use `show_window` to make it visible.
    """
    if not glfw.init():
        raise Exception("GLFW initialization failed")
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(width, height, title, None, None)
    if window is None:
        terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)
    return window
