from os.path import dirname
from glfw import wait_events, terminate, window_should_close
from app.controller import Controller
from app.scene import Scene
from app.window import init_window
import sys


def main():
    window = init_window(940, 1000, "Program")
    config_path = (
        f"{dirname(__file__)}/objects/config.toml"
        if len(sys.argv) <= 1
        else sys.argv[1]
    )
    scene = Scene(window, config_path)
    controller = Controller(scene)

    # Main loop
    while not window_should_close(window):
        scene.draw()
        wait_events()
        controller.log()

    terminate()


if __name__ == "__main__":
    main()
