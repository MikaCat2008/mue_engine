from math import ceil
from typing import Optional
from collections import deque, defaultdict

import pygame as pg
from pygame.surface import Surface

from .tile import Tile
from .sprite import Sprite
from .render_chunk import RenderChunk


class LayerData:
    tiles: dict[tuple[int, int], Tile]
    chunks: dict[tuple[int, int], RenderChunk]
    sprites: dict[int, Sprite]
    surface: Surface
    centrize: bool

    def __init__(self, size: tuple[int, int], centrize: bool) -> None:
        self.tiles = {}
        self.chunks = {}
        self.sprites = {}
        self.surface = Surface(size, pg.SRCALPHA)
        self.centrize = centrize

    def create_sprite(
        self, 
        z_index: int, 
        surface: Surface, 
        position: tuple[int, int]
    ) -> int:
        sprite = Sprite(z_index, surface, position)

        self.sprites[id(sprite)] = sprite

        return id(sprite)
    
    def update_sprite(
        self, 
        sprite_id: int,
        z_index: Optional[int] = None,
        surface: Optional[Surface] = None,
        position: Optional[tuple[int, int]] = None
    ) -> None:
        sprite = self.sprites[sprite_id]

        if z_index is not None and z_index != sprite.z_index:
            sprite.z_index = z_index
            sprite.requires_render = True

        if surface:
            sprite.surface = surface
            sprite.requires_render = True

        if position and position != sprite.position:                
            sprite.position = position
            sprite.requires_update_covered_tiles = True

    def remove_sprite(self, sprite_id: int) -> None:
        self.sprites[sprite_id].is_alive = False

    def get_tile_at(self, position: tuple[int, int]) -> Tile:
        if position in self.tiles:
            return self.tiles[position]
        else:
            tile = Tile(position)

            self.tiles[position] = tile

            if tile.chunk_position not in self.chunks:
                self.chunks[tile.chunk_position] = RenderChunk(tile.chunk_position)

            return tile

    def get_covered_tiles(self, sprite: Sprite) -> set[tuple[int, int]]:
        x, y = sprite.position
        w, h = sprite.surface.get_size()

        if self.centrize:
            x -= w // 2
            y -= h // 2

        min_x = x // 16
        min_y = y // 16

        max_x = ceil((x + w) / 16)
        max_y = ceil((y + h) / 16)
        
        return {
            (tx, ty)
            for tx in range(min_x, max_x)
            for ty in range(min_y, max_y)
        }

    def update_tiles(self) -> None:
        remove_sprites = deque()

        for sprite in self.sprites.values():
            if not (
                (not sprite.is_alive) or
                sprite.requires_render or
                sprite.requires_update_covered_tiles 
            ): 
                continue

            covered_tiles = sprite.covered_tiles

            if (not sprite.is_alive) or sprite.requires_update_covered_tiles:
                if sprite.is_alive:
                    new_covered_tiles = self.get_covered_tiles(sprite)
                else:
                    new_covered_tiles = set()

                for position in covered_tiles | new_covered_tiles:
                    tile = self.get_tile_at(position)

                    if position in covered_tiles and position in new_covered_tiles:
                        tile.requires_render = True
                    if position in covered_tiles:
                        tile.remove_sprite(sprite)
                    if position in new_covered_tiles:
                        tile.add_sprite(sprite)

                sprite.covered_tiles = new_covered_tiles
                sprite.requires_render = False
                sprite.requires_update_covered_tiles = False

            if sprite.requires_render:
                for position in sprite.covered_tiles:
                    tile = self.get_tile_at(position)
                    tile.requires_render = True

                sprite.requires_render = False

        if remove_sprites:
            remove_sprites_set = set(remove_sprites)

            self.sprites = {
                sprite_id: sprite
                for sprite_id, sprite in self.sprites
                if sprite_id not in remove_sprites_set
            }

        requires_render_chunks: dict[tuple[int, int], deque[Tile]] = defaultdict(deque)
        
        for tile in (tile for tile in self.tiles.values() if tile.requires_render):
            requires_render_chunks[tile.chunk_position].append(tile)

            tile.sort_sprites()
            tile.requires_render = False

        for chunk, tiles in requires_render_chunks.items():
            self.chunks[chunk].render_tiles(tiles, self.centrize)

        self.tiles = {
            position: tile
            for position, tile in self.tiles.items()
            if tile.sprites
        }

    def render_chunks(self, offset: tuple[int, int]) -> None:
        ox, oy = offset

        self.surface.fill((0, 0, 0, 0))
        self.surface.fblits(
            (
                chunk.surface,
                (
                    chunk.render_position[0] - ox,
                    chunk.render_position[1] - oy
                )
            )
            for chunk in self.chunks.values()
        )
