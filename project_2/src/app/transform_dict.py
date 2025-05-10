from collections.abc import Iterable, Mapping
from copy import copy
from typing import Any, Callable, final, override


@final
class TransformDict(dict[str, float]):
    _on_change: Callable[[], None] | None

    def __init__(
        self,
        *args: Iterable[tuple[str, float]] | Mapping[str, float],
        on_change: Callable[[], None] | None = None,
        **kwargs: float,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._on_change = on_change

    @override
    def __setitem__(self, key: str, value: float) -> None:
        super().__setitem__(key, value)
        if self._on_change:
            self._on_change()

    @override
    def update(self, *args: Any, **kwargs: float) -> None:
        if len(args) > 1:
            raise TypeError(
                f"update expected at most 1 argument, got {len(args)}"
            )

        if args:
            other = args[0]
            if isinstance(other, Mapping):
                for key in other:
                    self[key] = other[key]  # pyright: ignore [reportArgumentType]
            else:
                for key, value in other:
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value

        if self._on_change:
            self._on_change()

    def __copy__(self) -> "TransformDict":
        new_dict = TransformDict(self, on_change=None)
        new_dict._on_change = self._on_change
        return new_dict

    def __deepcopy__(
        self, memo: dict[int, object] | None = None
    ) -> "TransformDict":
        if memo is None:
            memo = {}
        new_dict = TransformDict(self, on_change=copy(self._on_change))
        memo[id(self)] = new_dict  # helps with recursive copying
        return new_dict
