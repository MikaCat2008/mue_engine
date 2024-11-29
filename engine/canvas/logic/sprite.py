from pygame.surface import Surface


class Sprite:
    z_index: int
    surface: Surface
    is_alive: bool
    position: tuple[int, int]
    covered_tiles: set[tuple[int, int]]
    requires_render: bool
    requires_update_covered_tiles: bool

    def __init__(
        self, z_index: int, surface: Surface, position: tuple[int, int]
    ) -> None:
        self.z_index = z_index
        self.surface = surface
        self.is_alive = True
        self.position = position
        self.covered_tiles = set()
        self.requires_render = True
        self.requires_update_covered_tiles = True
