from __future__ import annotations

from typing import TYPE_CHECKING

from engine.singleton import Singleton

if TYPE_CHECKING:
    from engine.executor import Executor


class System(Singleton):
    executor: Executor

    _instance: System

    def load(self) -> None:
        ...

    def start(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
