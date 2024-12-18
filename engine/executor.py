from time import time
from typing import Optional

from .core import Entity, System

UPS = 120


class Executor:
    body: Entity
    systems: list[System]

    def __init__(self, body: Entity, systems: Optional[list[System]] = None) -> None:
        self.body = body
        self.systems = systems or []

    def start(self) -> None:
        for system in self.systems:
            system.executor = self

        for system in self.systems:
            system.load()

        self.start_entity(self.body)

        for system in self.systems:
            system.start()

    def start_entity(self, entity: Entity) -> None:
        entity.start()

        for child in entity.childs:
            self.start_entity(child)

    def loop(self) -> None:
        current_time = time()
        
        while 1:
            last_time, current_time = current_time, time()
            delta = current_time - last_time

            for system in self.systems:
                system.update(delta)
        
    def run(self) -> None:
        self.start()
        self.loop()
