from .entities import (
    Body,
    Container
)
from .components import (
    Identity,
    Transform
)
from .systems import (
    TimerSystem,
    SearchSystem,
    RenderSystem,
    ResourcesSystem
)


ENTITIES = {
    "body": Body, 
    "container": Container
}

COMPONENTS = {
    "Identity": Identity,
    "Transform": Transform
}

SYSTEMS = [
    TimerSystem(),
    SearchSystem(),
    RenderSystem(),
    ResourcesSystem()
]
