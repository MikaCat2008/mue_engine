from typing import Optional
from collections import deque

import pygame as pg
from pygame.time import Clock
from pygame.event import get as get_events
from pygame.surface import Surface
from pygame.display import flip as flip_display, set_mode

from engine.core import Entity, System
from engine.base import RenderSystem
from engine.executor import Executor


class PygameExecutor(Executor):
    screen: Surface
    max_ups: int

    def __init__(
        self, 
        body: Entity, 
        systems: Optional[list[System]] = None,
        max_ups: int = 120
    ) -> None:
        super().__init__(body, systems)

        self.max_ups = max_ups

    def start(self) -> None:
        self.screen = set_mode((512, 288), pg.SCALED | pg.DOUBLEBUF | pg.FULLSCREEN)

        super().start()

    def loop(self) -> None:
        clock = Clock()
        render = RenderSystem()

        delta = 1 / self.max_ups

        while 1:
            for event in get_events():
                if event.type == pg.QUIT:
                    pg.quit()

            for system in self.systems:
                system.update(delta)

            self.screen.fill((0, 0, 0))
            self.screen.blits((
                (surface, position)
                for _, surface, position in sorted(
                    render.render_datas,
                    key=lambda render_data: render_data[0]
                )
            ), 0)
            
            render.render_datas = deque()

            flip_display()

            delta = clock.tick(self.max_ups) / 1000
