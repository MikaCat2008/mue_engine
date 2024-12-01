from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame.surface import Surface

from engine.core import System
from engine.base.components import Identity
from engine.base.systems import SearchSystem, ResourcesSystem

if TYPE_CHECKING:
    from .layer import CanvasLayer
    from .entity import CanvasEntity

from .logic import LayerData
from .layer_data import CanvasLayerData
from .entity_identity import CanvasEntityIdentity

from .builder_component_sprite import BuilderComponent_Sprites


class CanvasLayerSystem(System):
    layers: dict[str, LayerData]

    def __init__(self) -> None:
        self.layers = {}

    def _create_layer_data(self, layer_tag: str) -> LayerData:
        search = SearchSystem()

        layer = search.search_by_tag(layer_tag)
        layer_data = layer.get_component(CanvasLayerData)
        
        return LayerData(layer_data.size, layer_data.use_sprite_centrize)

    def _get_layer_data(self, entity: CanvasEntity) -> LayerData:
        identity = entity.get_component(CanvasEntityIdentity)
        layer = identity.layer

        if layer not in self.layers:
            self.layers[layer] = self._create_layer_data(layer)
        
        return self.layers[layer]

    def start_entity(self, entity: CanvasEntity) -> None:
        sprites = entity.get_component(BuilderComponent_Sprites)

        if sprites is None:
            return

        for sprite in sprites.sprites:
            self.create_sprite(
                entity,
                sprite.z_index,
                sprite.texture,
                sprite.position,
                sprite.rotation,
                sprite.sprite_tag            
            )

        entity.remove_component(BuilderComponent_Sprites)

    def create_sprite(
        self, 
        entity: CanvasEntity, 
        z_index: int,
        texture: str, 
        position: tuple[int, int],
        rotation: int,
        sprite_tag: str
    ) -> None:
        resources = ResourcesSystem()

        surface = resources.get_texture(texture, rotation)

        layer_data = self._get_layer_data(entity)
        sprite_id = layer_data.create_sprite(z_index, surface, position)

        identity = entity.get_component(CanvasEntityIdentity)
        identity.sprites[sprite_tag] = sprite_id

    def update_sprite(
        self,
        entity: CanvasEntity,
        sprite_tag: str,
        z_index: Optional[int] = None,
        texture: Optional[str] = None,
        position: Optional[tuple[int, int]] = None,
        rotation: Optional[int] = None
    ) -> None:
        resources = ResourcesSystem()

        identity = entity.get_component(CanvasEntityIdentity)
        sprite_id = identity.sprites[sprite_tag]

        if texture is None or rotation is None:
            surface = None
        else:
            surface = resources.get_texture(texture, rotation)

        layer_data = self._get_layer_data(entity)
        layer_data.update_sprite(sprite_id, z_index, surface, position)

    def remove_sprite(
        self,
        entity: CanvasEntity,
        sprite_tag: str
    ) -> None:
        identity = entity.get_component(CanvasEntityIdentity)
        sprite_id = identity.sprites[sprite_tag]
        del identity.sprites[sprite_tag]

        layer_data = self._get_layer_data(entity)
        layer_data.remove_sprite(sprite_id)

    def update_tiles(self, layer: CanvasLayer) -> None:
        identity = layer.get_component(Identity)
        tag = identity.tag

        if tag not in self.layers:
            layer_data = layer.get_component(CanvasLayerData)

            self.layers[tag] = LayerData(layer_data.size, layer_data.use_sprite_centrize)

        self.layers[tag].update_tiles()

    def render_chunks(
        self, 
        layer: CanvasLayer,
        offset: tuple[int, int],
        canvas_surface: Surface 
    ) -> None:
        identity = layer.get_component(Identity)
        canvas_layer_data = layer.get_component(CanvasLayerData)

        if not canvas_layer_data.use_offset:
            offset = 0, 0

        layer_data = self.layers[identity.tag]
        layer_data.render_chunks(offset)
        
        canvas_surface.blit(layer_data.surface)
