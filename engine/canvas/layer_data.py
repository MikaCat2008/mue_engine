from engine.core import Component


class CanvasLayerData(Component):
    size: tuple[int, int]
    z_index: int
    use_offset: bool
    use_sprite_centrize: bool

    def __init__(
        self, 
        size: tuple[int, int], 
        z_index: int, 
        use_offset: bool = True,
        use_sprite_centrize: bool = True
    ) -> None:
        self.size = size
        self.z_index = z_index
        self.use_offset = use_offset
        self.use_sprite_centrize = use_sprite_centrize
