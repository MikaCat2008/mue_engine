from engine.core import Component


class CanvasData(Component):
    size: tuple[int, int]
    
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
