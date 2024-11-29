from engine.core import Component


class CanvasData(Component):
    size: tuple[int, int]
    offset: tuple[int, int]
    
    def __init__(
        self, 
        size: tuple[int, int], 
        offset: tuple[int, int] = (0, 0)
    ) -> None:
        self.size = size
        self.offset = offset
