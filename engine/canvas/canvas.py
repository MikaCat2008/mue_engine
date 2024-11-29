from collections import deque

from engine.core import Entity

from .layer import CanvasLayer
from .system import CanvasSystem


class Canvas(Entity):
    childs: deque[CanvasLayer]

    def start(self) -> None:
        system = CanvasSystem()
        system.add_canvas(self)

    def update_offset(self, offset: tuple[int, int]) -> None:
        system = CanvasSystem()
        system.update_offset(self, offset)
