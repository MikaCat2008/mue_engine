from __future__ import annotations

from typing import TYPE_CHECKING

from engine.core import Entity

if TYPE_CHECKING:
    from .entity import CanvasEntity

from .layer_system import CanvasLayerSystem


class CanvasLayer(Entity):
    def add_canvas_entity(self, entity: CanvasEntity) -> None:
        canvas_layer_system = CanvasLayerSystem()
        canvas_layer_system.add_canvas_entity(self, entity)

    def remove_canvas_entity(self, entity: CanvasEntity) -> None:
        canvas_layer_system = CanvasLayerSystem()
        canvas_layer_system.remove_canvas_entity(self, entity)
