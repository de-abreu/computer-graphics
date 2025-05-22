from collections.abc import Iterable, Mapping
from copy import copy
from typing import Any, Callable, final, override


@final
class TransformDict(dict[str, float]):
    """
    An observable dictionary that triggers a callback when modified.

    This extends `dict[str, float]` and calls a callback function whenever
    items are set or updated. Useful for tracking transformations in 3D graphics.

    Attributes
    ----------
    _on_change : Callable[[], None] | None
        Optional callback function triggered on dictionary modifications.
    """
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
        """
        Set a key-value pair and trigger the callback if defined.

        Parameters
        ----------
        key : str
            The dictionary key to set.
        value : float
            The value to associate with the key.
        """
        super().__setitem__(key, value)
        if self._on_change:
            self._on_change()

    @override
    def update(self, *args: Any, **kwargs: float) -> None:
        """
        Update the dictionary with new key-value pairs and trigger the callback.

        Parameters
        ----------
        *args : Union[Iterable[tuple[str, float]], Mapping[str, float]]
            Positional arguments (either a mapping or iterable of pairs).
        **kwargs : float
            Keyword arguments representing key-value pairs.

        Raises
        ------
        TypeError
            If more than one positional argument is provided.
        """
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
        """
        Create a shallow copy of the dictionary.

        Returns
        -------
        TransformDict
            A new dictionary with the same items and callback reference.
        """
        new_dict = TransformDict(self, on_change=None)
        new_dict._on_change = self._on_change
        return new_dict

    def __deepcopy__(
        self, memo: dict[int, object] | None = None
    ) -> "TransformDict":
        """
        Create a deep copy of the dictionary.

        Parameters
        ----------
        memo : dict[int, object] | None
            Memo dictionary for tracking copied objects (used internally).

        Returns
        -------
        TransformDict
            A new dictionary with deep copies of items and callback.
        """
        if memo is None:
            memo = {}
        new_dict = TransformDict(self, on_change=copy(self._on_change))
        memo[id(self)] = new_dict  # helps with recursive copying
        return new_dict
