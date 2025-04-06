import os
from tabulate import tabulate
from .objects.object import Object


class Logger:
    objects: list[Object]
    last_state: list[list[str]]
    last_controlled_index: int

    def __init__(self, objects: list[Object]) -> None:
        self.objects = objects
        self.last_state = self._get_state()
        self.last_controlled_index = 0

    def _get_state(self) -> list[list[str]]:
        state: list[list[str]] = []
        for i, obj in enumerate(self.objects):
            state.append(
                [
                    f"Object {i + 1}",
                    f"({obj.position['x']:.2f}, {obj.position['y']:.2f}, {obj.position['z']:.2f})",
                    f"({obj.rotation['x']:.2f}, {obj.rotation['y']:.2f}, {obj.rotation['z']:.2f})",
                    f"{obj.scale:.2f}",
                ]
            )
        return state

    def _clear_terminal(self) -> None:
        _ = os.system("clear")

    def log(self, controlled_index: int) -> None:
        current_state = self._get_state()
        if (
            current_state != self.last_state
            or controlled_index != self.last_controlled_index
        ):
            self._clear_terminal()
            headers = ["Object", "Position (x, y, z)", "Rotation (x, y, z)", "Scale"]
            print(tabulate(current_state, headers=headers, tablefmt="grid"))
            print(f"\nCurrently controlling: Object {controlled_index + 1}\n")
            self.last_state = current_state
            self.last_controlled_index = controlled_index
