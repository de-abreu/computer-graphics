from app.object import Object
from app.utils import ObjectConfig as Config, BufferData


class Light(Object):
    color: tuple[float, float, float]
    intensity: float
    current: float

    def __init__(self, id: int, config: Config, bd: BufferData):
        super().__init__(id, config, bd)
        self.color = config.emission_color
        self.current = self.intensity = config.emission_intensity

    def toggle(self) -> None:
        self.current = self.intensity if self.current < 0.01 else 0.0
