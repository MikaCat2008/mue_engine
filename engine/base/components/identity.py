from engine.core import Component


class Identity(Component):
    tag: str
    name: str

    def __init__(self, tag: str = "", name: str = "") -> None:
        self.tag = tag
        self.name = name
