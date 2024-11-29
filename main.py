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

from engine.canvas import (
    Canvas,
    CanvasData,
    CanvasEntity,

    ENTITIES as CANVAS_ENTITIES,
    COMPONENTS as CANVAS_COMPONENTS,
    SYSTEMS as CANVAS_SYSTEMS
)


class Player(CanvasEntity):
    ...


class StartSystem(System):
    canvas: Canvas
    player: Player
    player_position: tuple[int, int]

    def load(self) -> None:
        resources = ResourcesSystem()
        resources.load_texture("player.0", "assets/player/0.png")

    def start(self) -> None:
        search = SearchSystem()

        self.canvas = search.search_by_tag("main-canvas")
        self.player = search.search_by_tag("main-player")
        self.player_position = 100, 100

    def update(self, delta: float) -> None:
        data = self.canvas.get_component(CanvasData)
        ox, oy = data.offset

        px, py = self.player_position
        mx, my = get_pos()
        mx += ox
        my += oy

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
        ix, iy = int(position[0]), int(position[1])

        rotation = atan2(py - my, mx - px) * 180 / pi

        self.canvas.update_offset((ix - 512 // 2, iy - 288 // 2))
        self.player.update_sprite(
            "sprite", 
            texture="player.0", 
            position=(ix, iy), 
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
