from glfw import wait_events, terminate, window_should_close
from app.controller import init_controller
from app.scene import Scene
from app.window import init_window
import sys


def main():
    window = init_window(940, 1000, "Program")
    config_path = (
        f"{__file__}/objects/config.toml" if len(sys.argv) <= 1 else sys.argv[1]
    )
    scene = Scene(window, config_path)
    init_controller(window)

    # Main loop
    while not window_should_close(window):
        scene.draw(window)
        wait_events()
        scene.log()

    terminate()


if __name__ == "__main__":
    main()
