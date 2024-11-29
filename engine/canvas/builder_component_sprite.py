from collections import deque

from engine.core import Component


class BuilderSprite:
    z_index: int
    texture: str
    position: tuple[int, int]
    rotation: int
    sprite_tag: str

    def __init__(
        self, 
        z_index: int, 
        texture: str, 
        position: tuple[int, int], 
        rotation: int,
        sprite_tag: str
    ) -> None:
        self.z_index = z_index
        self.texture = texture
        self.position = position
        self.rotation = rotation
        self.sprite_tag = sprite_tag


class BuilderComponent_Sprites(Component):
    sprites: deque[BuilderSprite]

    def __init__(self) -> None:
        self.sprites = deque()
