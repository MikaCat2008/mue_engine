from typing import Optional

from pygame.surface import Surface

from engine.core import Entity

from .layer import CanvasLayerSystem


class CanvasEntity(Entity):
    def create_sprite(
        self, 
        z_index: int,
        texture: str, 
        position: tuple[int, int],
        rotation: int,
        sprite_tag: str
    ) -> None:
        canvas_entity_system = CanvasLayerSystem()
        canvas_entity_system.create_sprite(
            self, z_index, texture, position, rotation, sprite_tag
        )

    def update_sprite(
        self, 
        sprite_tag: str, 
        z_index: Optional[int] = None,
        texture: Optional[str] = None,
        position: Optional[tuple[int, int]] = None,
        rotation: Optional[int] = None
    ) -> None:
        layer_system = CanvasLayerSystem()
        layer_system.update_sprite(
            self, sprite_tag, z_index, texture, position, rotation
        )

    def remove_sprite(self, sprite_id: int) -> None:
        canvas_entity_system = CanvasLayerSystem()
        canvas_entity_system.remove_sprite(self, sprite_id)
