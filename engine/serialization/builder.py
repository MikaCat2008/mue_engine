from collections import deque

from .tokenizer import Tokenizer
from .syntax_tree import Node, SyntaxTree

from ..core import Entity, Component
from .factory import EntityFactory, ComponentFactory


class Builder:
    entities: EntityFactory
    components: ComponentFactory

    def __init__(self, entities: EntityFactory, components: ComponentFactory) -> None:
        self.entities = entities
        self.components = components

        self.tokenizer = Tokenizer()
        self.syntax_tree = SyntaxTree()

    def build_entity_from_node(self, node: Node) -> Entity:
        entity = self.entities.create(node.name)

        childs = node.sections.get("childs", deque())
        components = node.sections.get("components", deque())

        entity.childs = self.build_entities_from_nodes(childs)
        
        for component in self.build_components_from_nodes(components):
            entity.add_component(component)

        return entity

    def build_entities_from_nodes(self, nodes: deque[Node]) -> deque[Entity]:
        entities = deque()

        for node in nodes:
            entities.append(self.build_entity_from_node(node))
        
        return entities

    def build_component_from_node(self, node: Node) -> Component:
        properties = {
            child.attributes["name"]: child.attributes["value"]
            for child in node.sections.get(None, deque())
            if child.name == "property"
        }

        return self.components.create(
            node.name, **properties
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
