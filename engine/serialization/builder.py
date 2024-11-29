from typing import Optional
from collections import deque

from .tokenizer import Tokenizer
from .syntax_tree import Node, SyntaxTree

from ..core import Entity, Component
from .factory import EntityFactory, ComponentFactory

from engine.canvas import BuilderSprite, BuilderComponent_Sprites


class Builder:
    entities: EntityFactory
    components: ComponentFactory

    def __init__(self, entities: EntityFactory, components: ComponentFactory) -> None:
        self.entities = entities
        self.components = components

        self.tokenizer = Tokenizer()
        self.syntax_tree = SyntaxTree()

    def get_properties(self, section: dict[Optional[str], deque[Node]]) -> dict[str, object]:
        return {
            child.attributes["name"]: child.attributes["value"]
            for child in section
            if child.name == "property"
        }

    def handle_section(self, name: str, entity: Entity, section: deque[Node]) -> None:
        if name == "childs":
            entity.childs = self.build_entities_from_nodes(section)
        
        elif name == "components":
            for component in self.build_components_from_nodes(section):
                entity.add_component(component)

        elif name == "sprites":
            component = BuilderComponent_Sprites()
            
            for node in section:
                if node.name != "Sprite":
                    continue

                properties = self.get_properties(
                    node.sections.get(None, deque())
                )

                z_index = properties.get("z_index", 0)
                texture = properties.get("texture", "")
                position = properties.get("position", (0, 0))
                rotation = properties.get("rotation", 0)
                sprite_tag = properties.get("sprite_tag", "")

                component.sprites.append(
                    BuilderSprite(
                        z_index, texture, position, rotation, sprite_tag
                    )
                )

            entity.add_component(component)

    def build_entity_from_node(self, node: Node) -> Entity:
        entity = self.entities.create(node.name)

        for name, section in node.sections.items():
            self.handle_section(name, entity, section)

        return entity

    def build_entities_from_nodes(self, nodes: deque[Node]) -> deque[Entity]:
        entities = deque()

        for node in nodes:
            entities.append(self.build_entity_from_node(node))
        
        return entities

    def build_component_from_node(self, node: Node) -> Component:
        return self.components.create(
            node.name, 
            **self.get_properties(
                node.sections.get(None, deque())
            )
        )

    def build_components_from_nodes(self, nodes: deque[Node]) -> deque[Component]:
        components = deque()

        for node in nodes:
            components.append(self.build_component_from_node(node))

        return components

    def build_entities_from_text(self, text: str) -> deque[Entity]:
        tokens = self.tokenizer.tokenize(text)
        nodes = self.syntax_tree.parse(tokens)[None]

        return self.build_entities_from_nodes(nodes)
