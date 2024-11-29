from collections import deque

from engine.core import Component


class CanvasEntityIdentity(Component):
    layer: str
    sprites: dict[str, int]

    def __init__(self, layer: str) -> None:
        self.layer = layer
        self.sprites = {}
