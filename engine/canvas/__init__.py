from .data import CanvasData
from .canvas import Canvas as Canvas
from .system import CanvasSystem as CanvasSystem

from .layer import CanvasLayer as CanvasLayer
from .layer_data import CanvasLayerData as CanvasLayerData
from .layer_system import CanvasLayerSystem as CanvasLayerSystem

from .entity import CanvasEntity as CanvasEntity
from .entity_identity import CanvasEntityIdentity as CanvasEntityIdentity

ENTITIES = {
    "Canvas": Canvas,
    "CanvasLayer": CanvasLayer,
    "CanvasEntity": CanvasEntity
}

COMPONENTS = {
    "CanvasData": CanvasData,
    "CanvasLayerData": CanvasLayerData,
    "CanvasEntityIdentity": CanvasEntityIdentity
}

SYSTEMS = [
    CanvasSystem(),
    CanvasLayerSystem()
]
