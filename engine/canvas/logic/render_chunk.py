from typing import Generator
from itertools import chain
from collections import deque

import pygame as pg
from pygame.surface import Surface

from .tile import Tile

black_rect = Surface((16, 16))


class RenderChunk:
    surface: Surface
    position: tuple[int, int]
    render_position: tuple[int, int]

    def __init__(self, position: tuple[int, int]) -> None:
        x, y = position
        
        self.surface = Surface((128, 128), pg.SRCALPHA)
        self.position = position
        self.render_position = x * 128, y * 128

    def render_tiles(self, tiles: deque[Tile]) -> None:
        self.surface.blits(chain(
            (
                (black_rect, tile.render_position)
                for tile in tiles
            ),
            (
                render_data
                for tile in tiles
                for render_data in self.get_render_data(tile)
            )
        ), 0)

    def get_render_data(self, tile: Tile) -> Generator[
        tuple[
            Surface, tuple[int, int], tuple[int, int, int, int]
        ],
        None, 
        None
    ]:
        x, y = tile.position
        arx, ary = x * 16, y * 16

        return (
            (
                sprite.surface,
                tile.render_position,
                (
                    arx - sprite.position[0] + sprite.surface.get_width() // 2,
                    ary - sprite.position[1] + sprite.surface.get_height() // 2,
                    16, 16
                )
            )
            for sprite in tile.sprites
        )
