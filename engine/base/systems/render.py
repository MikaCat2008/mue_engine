from collections import deque

from pygame.surface import Surface

from engine.core import System

RenderDataType = tuple[int, Surface, tuple[int, int]]


class RenderSystem(System):
    render_datas: deque[RenderDataType]

    def __init__(self) -> None:
        self.render_datas = deque()

    def add_render_datas(self, render_datas: deque[RenderDataType]) -> None:
        self.render_datas.extend(render_datas)
