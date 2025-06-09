from app.object import Object
from app.utils import ObjectConfig as Config, BufferData
from app.utils.dataclasses import ReflectionCoefficients


class Light(Object):
    """
    A light source in the scene that can be toggled on or off.
    """

    _on: bool = False
    _default: ReflectionCoefficients

    def __init__(self, id: int, config: Config, bd: BufferData):
        """Initialize the Light object.

        Parameters
        ----------
        id : int
            Unique identifier for the object.
        config : Config
            Configuration containing illumination properties.
        bd : BufferData
            Buffer data for the object.
        """
        super().__init__(id, config, bd)
        self._default = config.illumination_properties.reflection_coefficients
        self.toggle()

    def toggle(self) -> None:
        """Toggle the light on or off.

        Notes
        -----
        When turned on, the light uses high reflection coefficients for emission.
        When turned off, it reverts to the default reflection coefficients.
        """
        if self._on:
            self.illumination.reflection_coefficients = self._default
        else:
            self.illumination.reflection_coefficients = ReflectionCoefficients(
                1.0, 1.0, 1.0, 1000.0
            )
        self._on = not self._on

    @property
    def intensity(self) -> float:
        if self._on:
            return self.illumination.emission_intensity
        return 0.0

    @property
    def on(self) -> bool:
        return self._on
