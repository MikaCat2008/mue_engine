from collections import deque

from .sprite import Sprite


class Tile:
    sprites: deque[Sprite]
    position: tuple[int, int]
    chunk_position: tuple[int, int]
    render_position: tuple[int, int]
    requires_render: bool

    def __init__(self, position: tuple[int, int]) -> None:
        x, y = position

        self.sprites = deque()
        self.position = position
        self.chunk_position = x // 8, y // 8
        self.render_position = x % 8 * 16, y % 8 * 16
        self.requires_render = True

    def sort_sprites(self) -> None:
        self.sprites = deque(sorted(self.sprites, key=lambda sprite: sprite.z_index))

    def add_sprite(self, sprite: Sprite) -> None:
        self.sprites.append(sprite)
        self.requires_render = True

    def remove_sprite(self, sprite: Sprite) -> None:
        self.sprites.remove(sprite)
        self.requires_render = True
