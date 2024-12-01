from collections import deque

from engine.core import Entity
from engine.serialization import Node, get_properties

from .builder_component_sprite import BuilderSprite, BuilderComponent_Sprites


def handle_sprites_section(entity: Entity, section: deque[Node]) -> None:
    component = BuilderComponent_Sprites()
            
    for node in section:
        if node.name != "Sprite":
            continue

        properties = get_properties(
            node.sections.get(None, deque())
        )

        z_index = properties.get("z_index", 0)
        texture = properties.get("texture", "")
        position = properties.get("position", (0, 0))
        rotation = properties.get("rotation", 0)
        sprite_tag = properties.get("sprite_tag", "sprite")

        component.sprites.append(
            BuilderSprite(
                z_index, texture, position, rotation, sprite_tag
            )
        )

    entity.add_component(component)
