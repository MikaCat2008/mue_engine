from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..singleton import Singleton

if TYPE_CHECKING:
    from ..executor import Executor


class System(Singleton):
    executor: Executor

    _instance: System

    def load(self) -> None:
        ...

    def start(self) -> None:
        ...
    
    def update(self, delta: float) -> None:
        ...
