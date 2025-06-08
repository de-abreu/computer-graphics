from collections.abc import Iterable, Mapping

from typing import Any, Callable, override


class TransformDict(dict[str, float]):
    """
    A restricted dictionary that only allows "x", "y", and "z" keys.
    Triggers a callback when modified. Used for 3D transformations.

    Attributes
    ----------
    _on_change : Callable[[], None] | None
        Optional callback function triggered on dictionary modifications.
    """

    _on_change: Callable[[], None] | None
    _VALID_KEYS: set[str] = {"x", "y", "z"}

    def __init__(
        self,
        *args: Iterable[tuple[str, float]] | Mapping[str, float],
        on_change: Callable[[], None] | None = None,
        **kwargs: float,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._on_change = on_change
        # Validate initial keys
        for key in self:
            if key not in self._VALID_KEYS:
                raise KeyError(
                    f"Invalid key: {key}. Only 'x', 'y', 'z' allowed."
                )

    @override
    def __setitem__(self, key: str, value: float) -> None:
        """
        Set a key-value pair and trigger the callback if defined.
        Only allows "x", "y", or "z" as keys.

        Parameters
        ----------
        key : str
            The dictionary key to set.
        value : float
            The value to associate with the key.

                Raises
                ------
                KeyError
                    If the key is not "x", "y", or "z".
        """
        if key not in self._VALID_KEYS:
            raise KeyError(f"Invalid key: {key}. Only 'x', 'y', 'z' allowed.")
        super().__setitem__(key, value)
        if self._on_change:
            self._on_change()

    @override
    def update(self, *args: Any, **kwargs: float) -> None:
        """
        Update the dictionary with new key-value pairs and trigger the callback.
        Only allows "x", "y", or "z" as keys.

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
        KeyError
            If any key is not "x", "y", or "z".
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

    @override
    def copy(self) -> "TransformDict":
        """
        Create a shallow copy of the dictionary.

        Returns
        -------
        TransformDict
            A new dictionary with the same items and callback reference.
        """
        new_dict = TransformDict(self, on_change=self._on_change)
        return new_dict
