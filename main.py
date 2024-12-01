from __future__ import annotations

from math import pi, atan2
from random import randint

import pygame as pg
from pygame.key import get_pressed as get_key_pressed
from pygame.mouse import get_pos, get_pressed as get_mouse_pressed

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

    handle_sprites_section,

    ENTITIES as CANVAS_ENTITIES,
    COMPONENTS as CANVAS_COMPONENTS,
    SYSTEMS as CANVAS_SYSTEMS
)


class Tiles(CanvasEntity):
    ...


class Player(CanvasEntity):
    ...


class Structure(CanvasEntity):
    ...


class InventoryBar(CanvasEntity):
    ...


class StartSystem(System):
    def load(self) -> None:
        resources = ResourcesSystem()

        # ui

        resources.load_texture("ui.inventory_slot.0", "assets/ui/inventory_slot.0.png")
        resources.load_texture("ui.inventory_slot.1", "assets/ui/inventory_slot.1.png")

        # tiles

        resources.load_texture("tile.0.0", "assets/tile/0.0.png")
        resources.load_texture("tile.0.1", "assets/tile/0.1.png")
        resources.load_texture("tile.0.2", "assets/tile/0.2.png")

        resources.load_texture("tile.1.0", "assets/tile/1.0.png")
        resources.load_texture("tile.1.1", "assets/tile/1.1.png")
        resources.load_texture("tile.1.2", "assets/tile/1.2.png")
        resources.load_texture("tile.1.3", "assets/tile/1.3.png")

        # entity

        resources.load_texture("entity.player", "assets/entity/player.png")

        # structures

        resources.load_texture("structures.bath_tub", "assets/structures/bath_tub.png")
        resources.load_texture("structures.nightstand", "assets/structures/nightstand.png")


class PlayerControllerSystem(System):
    player: Player

    texture: str
    position: tuple[int, int]
    rotation: int

    def __init__(self) -> None:
        super().__init__()

        self.texture = "entity.player"
        self.position = 16, 16
        self.rotation = 0

    def start(self) -> None:
        search = SearchSystem()

        self.player = search.search_by_tag("main-player")

    def update(self, delta: float) -> None:
        x, y = self.position

        self.player.update_sprite(
            "sprite", 
            texture=self.texture, 
            position=(int(x), int(y)), 
            rotation=self.rotation
        )


class PlayerMovementSystem(System):
    def update(self, delta: float) -> None:
        ax, ay = 0, 0
        speed = 100 * delta
        state = get_key_pressed()

        if state[pg.K_a]:
            ax -= speed
        if state[pg.K_d]:
            ax += speed
        if state[pg.K_w]:
            ay -= speed
        if state[pg.K_s]:
            ay += speed

        controller = PlayerControllerSystem()

        px, py = controller.position
        controller.position = px + ax, py + ay


class PlayerRotationSystem(System):
    def update(self, delta: float) -> None:
        search = SearchSystem()
        controller = PlayerControllerSystem()
        
        canvas = search.search_by_tag("main-canvas")

        data = canvas.get_component(CanvasData)
        ox, oy = data.offset

        px, py = controller.position
        mx, my = get_pos()
        gmx = mx + ox
        gmy = my + oy

        controller.rotation = atan2(py - gmy, gmx - px) * 180 / pi


class CameraFollowingSystem(System):
    def update(self, delta: float) -> None:
        search = SearchSystem()
        controller = PlayerControllerSystem()
        
        canvas = search.search_by_tag("main-canvas")

        x, y = controller.position
        ix, iy = int(x), int(y)
        mx, my = get_pos()

        canvas.update_offset((
            ix - 512 // 2 + (mx - 512 // 2) // 8, 
            iy - 288 // 2 + (my - 288 // 2) // 8
        ))


class InventoryBarSystem(System):
    entity: InventoryBar
    slots_count: int
    first_slot_x: int
    first_slot_y: int
    current_slot_id: int

    def __init__(self) -> None:
        super().__init__()

        self.slots_count = 9
        self.first_slot_x = 256 - (self.slots_count // 2) * 15
        self.first_slot_y = 278
        self.current_slot_id = -1

    def start(self) -> None:
        search = SearchSystem()

        self.entity = search.search_by_tag("inventory-bar") 
        self.create_sprites()

    def create_sprites(self) -> None:
        for x in range(self.slots_count):
            self.entity.create_sprite(
                z_index=0, 
                texture="ui.inventory_slot.0", 
                position=(self.first_slot_x + x * 15, self.first_slot_y), 
                rotation=0, 
                sprite_tag=f"inventory-slot-{x}"
            )

    def select_slot(self, slot_index: int) -> None:
        if self.current_slot_id != -1:
            self.entity.update_sprite(
                f"inventory-slot-{self.current_slot_id}",
                z_index=0,
                texture="ui.inventory_slot.0",
                rotation=0
            )

        self.entity.update_sprite(
            f"inventory-slot-{slot_index}",
            z_index=1,
            texture="ui.inventory_slot.1",
            rotation=0,
        )
        self.current_slot_id = slot_index

    def update_key_control(self) -> None:
        state = get_key_pressed()

        for i in range(self.slots_count):
            if state[pg.K_1 + i]:
                self.select_slot(i)
                
                return

    def update_mouse_control(self) -> None:
        if not get_mouse_pressed()[0]:
            return
        
        mx, my = get_pos()
        ix = mx - self.first_slot_x + 8
        iy = my - self.first_slot_y + 8
        xo = 15 * (self.slots_count - 1)

        if ix < 1 or iy < 0 or ix > 16 + xo or iy > 15:
            return
        
        if ix == 0:
            slot_index = 0
        if ix == 16 + xo:
            slot_index = 4
        else:
            slot_index = (ix - 1) // 15

        if slot_index == self.current_slot_id:
            return

        self.select_slot(slot_index)

    def update(self, delta: float) -> None:
        self.update_key_control()
        self.update_mouse_control()


class TilesSystem(System):
    tiles: Tiles

    def start(self) -> None:
        search = SearchSystem()
        
        self.tiles = search.search_by_tag("tiles")
        self.create_sprites()

    def create_sprites(self) -> None:
        for x in range(32):
            for y in range(16):
                r = randint(0, 100)
                
                if r > 95:
                    tile_texture = 2
                elif r > 80:
                    tile_texture = 1
                elif r > 75:
                    tile_texture = 3
                else:
                    tile_texture = 0

                self.tiles.create_sprite(
                    z_index=0, 
                    texture=f"tile.1.{tile_texture}", 
                    position=(x * 16, y * 16), 
                    rotation=randint(0, 3) * 90, 
                    sprite_tag=f"tile-{x + y * 16}"
                )    


class StructuresSystem(System):
    def start(self) -> None:
        self.structures = {
            (10, 5): "bath_tub",

            (2, 4): "nightstand",
            (3, 4): "nightstand",
            (5, 4): "nightstand",
            (6, 4): "nightstand",

            (4, 4): "nightstand",

            (4, 2): "nightstand",
            (4, 3): "nightstand",
            (4, 5): "nightstand",
            (4, 6): "nightstand",

            (2, 2): "nightstand",
            (2, 3): "nightstand",
            
            (6, 5): "nightstand",
            (6, 6): "nightstand",

            (2, 6): "nightstand",
            (3, 6): "nightstand",

            (5, 2): "nightstand",
            (6, 2): "nightstand"
        }

        self.create_sprites()

    def create_sprites(self) -> None:
        for i, ((x, y), structure) in enumerate(self.structures.items()):
            x, y = position = x * 16, y * 16

            entity = builder.build_entities_from_text(
                f"""
                    <Structure>
                    sprites:
                        <Sprite>
                            <property name="texture" value="{structure}" />
                            <property name="position" value=v"{position}" />
                        </Sprite>
                    components:
                        <Identity>
                            <property name="tag" value="structure-{i}" />
                        </Identity>
                        <CanvasEntityIdentity>
                            <property name="layer" value="structures-layer" />
                        </CanvasEntityIdentity>
                    </Structure>
                """
            )[0]

            entity.create_sprite(
                z_index=0, 
                texture=f"structures.{structure}", 
                position=(x - 8, y - 8), 
                rotation=0, 
                sprite_tag=f"structure-{i}"
            )   


entity_factory = EntityFactory()
entity_factory.extend(BASE_ENTITIES | CANVAS_ENTITIES | {
    "Tiles": Tiles,
    "Player": Player,
    "Structure": Structure,
    "InventoryBar": InventoryBar
})

component_factory = ComponentFactory()
component_factory.extend(BASE_COMPONENTS | CANVAS_COMPONENTS)

text = open("body.ecsl").read()

builder = Builder(entity_factory, component_factory)
builder.add_section_handler("sprites", handle_sprites_section)

body = builder.build_entities_from_text(text)[0]

executor = PygameExecutor(body, systems=BASE_SYSTEMS + CANVAS_SYSTEMS + [
    StartSystem(),
    TilesSystem(),
    StructuresSystem(),
    InventoryBarSystem(),
    PlayerMovementSystem(),
    PlayerRotationSystem(),
    CameraFollowingSystem(),
    PlayerControllerSystem(),
], max_ups=2400)
executor.run()
