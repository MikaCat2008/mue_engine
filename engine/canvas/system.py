from __future__ import annotations

from typing import TYPE_CHECKING
from collections import deque

import pygame as pg
from pygame.surface import Surface

from engine.core import System
from engine.base.components import Identity, Transform
from engine.base.systems.render import RenderSystem, RenderDataType

if TYPE_CHECKING:
    from .canvas import Canvas

from .data import CanvasData
from .layer_system import CanvasLayerSystem


class CanvasSystem(System):
    canvases: dict[str, Canvas]
    canvases_surface: dict[str, Surface]

    def __init__(self) -> None:
        self.canvases = {}
        self.canvases_surface = {}

    def add_canvas(self, canvas: Canvas) -> None:
        data = canvas.get_component(CanvasData)
        identity = canvas.get_component(Identity)
        
        self.canvases[identity.tag] = canvas
        self.canvases_surface[identity.tag] = Surface(data.size, pg.SRCALPHA)

    def update_canvas(self, canvas: Canvas) -> None:
        identity = canvas.get_component(Identity)
        layer_system = CanvasLayerSystem()

        for layer in canvas.childs:
            layer_system.update_tiles(layer)

        surface = self.canvases_surface[identity.tag]
        surface.fill((0, 0, 0))

        data = canvas.get_component(CanvasData)
        offset = data.offset

        for layer in canvas.childs:
            layer_system.render_chunks(layer, offset, surface)

    def update_offset(self, canvas: Canvas, offset: tuple[int, int]) -> None:
        data = canvas.get_component(CanvasData)
        data.offset = offset

    def update(self, delta: float) -> None:
        for canvas in self.canvases.values():
            self.update_canvas(canvas)

        render = RenderSystem()
        render.add_render_datas(self.get_render_datas())

    def get_render_datas(self) -> deque[RenderDataType]:
        render_datas = deque()

        for canvas, surface in zip(
            self.canvases.values(), 
            self.canvases_surface.values()
        ):
            transform = canvas.get_component(Transform)
            
            render_datas.append(
                (transform.z_index, surface, transform.position)
            )

        return render_datas
