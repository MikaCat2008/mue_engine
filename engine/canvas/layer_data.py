from engine.core import Component


class CanvasLayerData(Component):
    size: tuple[int, int]

    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
