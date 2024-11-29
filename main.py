from __future__ import annotations

from math import pi, atan2

import pygame as pg
from pygame.key import get_pressed
from pygame.mouse import get_pos

from engine.core import System
from engine.serialization.factory import EntityFactory, ComponentFactory
from engine.serialization import Builder

from pygame_executor import PygameExecutor

from engine.base import (
    ENTITIES as BASE_ENTITIES, 
    COMPONENTS as BASE_COMPONENTS, 
    SYSTEMS as BASE_SYSTEMS
)

from engine.base.systems import SearchSystem, ResourcesSystem
from engine.base.components import Transform

from engine.canvas import (
    Canvas,
    CanvasEntity,

    ENTITIES as CANVAS_ENTITIES,
    COMPONENTS as CANVAS_COMPONENTS,
    SYSTEMS as CANVAS_SYSTEMS
)


class Player(CanvasEntity):
    ...


class StartSystem(System):
    player: Player
    player_position: tuple[int, int]

    def start(self) -> None:
        search = SearchSystem()
        resources = ResourcesSystem()

        resources.load_texture("player.0", "assets/player/0.png")

        canvas: Canvas = search.search_by_tag("main-canvas")
        canvas.add_to_system()

        player: Player = search.search_by_tag("main-player")
        player.create_sprite(
            0, "player.0", (100, 100), 0, "sprite"
        )

        self.player = player
        self.player_position = 100, 100

    def update(self, delta: float) -> None:
        px, py = self.player_position
        mx, my = get_pos()

        ax, ay = 0, 0
        speed = 100 * delta
        state = get_pressed()

        if state[pg.K_a]:
            ax -= speed
        if state[pg.K_d]:
            ax += speed
        if state[pg.K_w]:
            ay -= speed
        if state[pg.K_s]:
            ay += speed

        position = px + ax, py + ay
        rotation = atan2(py - my, mx - px) * 180 / pi

        self.player.update_sprite(
            "sprite", 
            texture="player.0", 
            position=(int(position[0]), int(position[1])), 
            rotation=rotation
        )
        self.player_position = position


entity_factory = EntityFactory()
entity_factory.extend(BASE_ENTITIES | CANVAS_ENTITIES | {
    "Player": Player
})

component_factory = ComponentFactory()
component_factory.extend(BASE_COMPONENTS | CANVAS_COMPONENTS)

text = open("body.ecsl").read()

builder = Builder(entity_factory, component_factory)
body = builder.build_entities_from_text(text)[0]

executor = PygameExecutor(body, systems=BASE_SYSTEMS + CANVAS_SYSTEMS + [
    StartSystem()
], max_ups=2400)
executor.run()
