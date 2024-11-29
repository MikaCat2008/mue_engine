from typing import Optional

from engine.core import Entity, System
from engine.base.components import Identity


class SearchSystem(System):
    def _search_by_tag(self, tag: str, entity: Entity) -> Optional[Entity]:
        identity = entity.get_component(Identity)
        
        if identity and identity.tag == tag:
            return entity
        
        for child in entity.childs:
            if _entity := self._search_by_tag(tag, child):
                return _entity

    def search_by_tag(self, tag: str) -> Optional[Entity]:
        return self._search_by_tag(tag, self.executor.body)
