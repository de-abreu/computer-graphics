from glfw import wait_events, terminate, window_should_close
from app.controller import init_controller
from app.object import ObjDescriptor
from app.scene import Scene
from app.window import init_window


def main():
    # Application initialization
    window = init_window(940, 1000, "Program")
    scene = Scene(window, [ObjDescriptor("Cabin")])
    init_controller(window)

    # Main loop
    while not window_should_close(window):
        scene.draw(window)
        wait_events()
        scene.log()

    terminate()


if __name__ == "__main__":
    main()
