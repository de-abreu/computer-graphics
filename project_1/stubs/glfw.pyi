from typing import Any

# Functions
def init() -> bool: ...
def terminate() -> None: ...
def create_window(
    width: int, height: int, title: str, monitor: Any | None, share: Any | None
) -> Any: ...
def show_window(window: Any) -> None: ...
def make_context_current(window: Any) -> None: ...
def window_should_close(window: Any) -> bool: ...
def window_hint(hint: int, value: int) -> None: ...
def poll_events() -> None: ...
def swap_buffers(window: Any) -> None: ...
def get_key(window: Any, key: int) -> int: ...

# Constants
KEY_A: int
KEY_D: int
KEY_F: int
KEY_G: int
KEY_I: int
KEY_J: int
KEY_K: int
KEY_L: int
KEY_O: int
KEY_P: int
KEY_R: int
KEY_S: int
KEY_T: int
KEY_U: int
KEY_W: int
KEY_X: int
KEY_Y: int
KEY_Z: int
PRESS: int
VISIBLE: int
FALSE: int

# ctypes
ctypes: Any
