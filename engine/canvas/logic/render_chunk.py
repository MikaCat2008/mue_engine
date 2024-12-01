from typing import Generator
from collections import deque

import pygame as pg
from pygame.draw import rect as draw_rect
from pygame.surface import Surface

from .tile import Tile


class RenderChunk:
    surface: Surface
    position: tuple[int, int]
    render_position: tuple[int, int]

    def __init__(self, position: tuple[int, int]) -> None:
        x, y = position
        
        self.surface = Surface((128, 128), pg.SRCALPHA)
        self.position = position
        self.render_position = x * 128, y * 128

    def render_tiles(self, tiles: deque[Tile], centrize: bool) -> None:
        self.surface.blits((
            render_data
            for tile in tiles
            for render_data in self.get_render_data(tile, centrize)
        ), 0)

    def get_render_data(self, tile: Tile, centrize: bool) -> Generator[
        tuple[
            Surface, tuple[int, int], tuple[int, int, int, int]
        ],
        None, 
        None
    ]:
        x, y = tile.position
        arx, ary = x * 16, y * 16

        draw_rect(
            self.surface, 
            (0, 0, 0, 0), 
            (x % 8 * 16, y % 8 * 16, 16, 16)
        )

        if centrize:
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
        return (
                (
                    sprite.surface,
                    tile.render_position,
                    (
                        arx - sprite.position[0],
                        ary - sprite.position[1],
                        16, 16
                    )
                )
                for sprite in tile.sprites
            )
