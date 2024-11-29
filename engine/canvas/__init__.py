from .data import CanvasData
from .canvas import Canvas as Canvas
from .system import CanvasSystem as CanvasSystem

from .layer import CanvasLayer as CanvasLayer
from .layer_data import CanvasLayerData as CanvasLayerData
from .layer_system import CanvasLayerSystem as CanvasLayerSystem

from .entity import CanvasEntity as CanvasEntity
from .entity_identity import CanvasEntityIdentity as CanvasEntityIdentity

from .builder_component_sprite import (
    BuilderSprite as BuilderSprite,
    BuilderComponent_Sprites as BuilderComponent_Sprites
)

ENTITIES = {
    "Canvas": Canvas,
    "CanvasLayer": CanvasLayer,
    "CanvasEntity": CanvasEntity
}

COMPONENTS = {
    "CanvasData": CanvasData,
    "CanvasLayerData": CanvasLayerData,
    "CanvasEntityIdentity": CanvasEntityIdentity,
    "BuilderComponent_Sprites": BuilderComponent_Sprites
}

SYSTEMS = [
    CanvasSystem(),
    CanvasLayerSystem()
]
