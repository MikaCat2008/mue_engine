from collections import deque

from engine.core import Entity

from .layer import CanvasLayer
from .system import CanvasSystem


class Canvas(Entity):
    childs: deque[CanvasLayer]

    def add_to_system(self) -> None:
        system = CanvasSystem()
        system.add_canvas(self)
