from pygame.image import load as load_image
from pygame.surface import Surface
from pygame.transform import rotate

from engine.core import System


class ResourcesSystem(System):
    textures: dict[str, Surface]
    cached_textures: dict[tuple[str, int], Surface]

    def __init__(self) -> None:
        self.textures = {}
        self.cached_textures = {}

    def load_texture(self, name: str, path: str) -> None:
        self.textures[name] = load_image(path).convert_alpha()

    def get_texture(self, name: str, rotation: int) -> Surface:
        data = name, rotation
        
        if data not in self.cached_textures:
            texture = self.textures[name]

            texture = rotate(texture, rotation)

            self.cached_textures[data] = texture
        
        return self.cached_textures[data]
