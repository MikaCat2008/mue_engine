from typing import Type, Callable
from collections import deque

from engine.core import Entity, Component, System
from engine.ecsl import Builder
from engine.ecsl.factory import EntityFactory, ComponentFactory


class BuilderSystem(System):
    builder: Builder

    def __init__(self) -> None:
        self.builder = Builder(
            EntityFactory(),
            ComponentFactory()
        )

    def add_section_handler(self, name: str, handler: Callable) -> None:
        self.builder.add_section_handler(name, handler)

    def build_entities_from_text(self, text: str) -> deque[Entity]:
        return self.builder.build_entities_from_text(text)
        
    def extend_entities(self, entities: dict[str, Type[Entity]]) -> None:
        self.builder.entities.extend(entities)

    def extend_components(self, components: dict[str, Type[Component]]) -> None:
        self.builder.components.extend(components)
