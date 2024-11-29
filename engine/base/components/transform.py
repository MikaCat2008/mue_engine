from engine.core import Component


class Transform(Component):
    z_index: int
    position: tuple[int, int]

    def __init__(
        self, 
        z_index: int = 0,
        position: tuple[int, int] = (0, 0)
    ) -> None:
        self.z_index = z_index
        self.position = position
