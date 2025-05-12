from glfw import wait_events, terminate, window_should_close
from app.controller import init_controller
from app.object import ObjDescriptor as desc
from app.scene import Scene
from app.window import init_window


def main():
    # INFO: Application initialization. List the models to use in the following
    # format, and add the necessary folders and files as described in the README:
    window = init_window(940, 1000, "Program")
    scene = Scene(
        window,
        [
            desc(
                "Sofa",
                initial_position=(-4.9, -2.6, -15.3),
                initial_rotation=(0.0, 3.0, 0.0),
                initial_scale=3.8,
            ),
            desc(
                "CoffeeTable",
                initial_position=(4.5, -2.4, 2.1),
                initial_scale=3.8,
            ),
            desc(
                "Chessboard",
                initial_position=(-0.5, -0.8, -6.5),
                initial_rotation=(0.0, -0.7, 0.0),
                initial_scale=0.01,
            ),
            desc("Bark"),
            desc("Leaves"),
            desc(
                "Well",
                initial_position=(3.5, -1.0, -28.6),
                initial_rotation=(0.0, 1.1, 0.0),
                initial_scale=1.5,
            ),
            desc(
                "PicnicTable",
                initial_position=(-4.6, 0.0, -23.5),
                initial_rotation=(0.0, 0.4, 0.0),
                initial_scale=0.03,
            ),
            desc(
                "Terrain", initial_position=(0.0, -0.8, -20), initial_scale=21.0
            ),
            desc(
                "Ceiling",
                initial_position=(-5.1, 5.9, -11.5),
                initial_rotation=(0.0, 3.0, 0.0),
                initial_scale=3.5,
            ),
            desc(
                "Floor",
                initial_position=(-5.1, -2.4, -11.5),
                initial_rotation=(0.0, 3.0, 0.0),
                initial_scale=3.5,
            ),
            desc(
                "Walls",
                initial_position=(-5.1, -2.4, -11.5),
                initial_rotation=(0.0, 3.0, 0.0),
                initial_scale=3.5,
            ),
            desc(
                "SkyDome",
                initial_scale=3.0,
            ),
        ],
    )
    init_controller(window)

    # Main loop
    while not window_should_close(window):
        scene.draw(window)
        wait_events()
        scene.log()

    terminate()


if __name__ == "__main__":
    main()
