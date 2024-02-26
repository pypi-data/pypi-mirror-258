from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, List, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .component import SingletonComponent, Component
    from .component_pool import ComponentPool
    from .entity import Entity

    T = TypeVar('T', bound=SingletonComponent)

class IEcsAdmin(ABC):
    @abstractmethod
    def get_component_pool(self, component_type: Type[Component]) -> ComponentPool:
        ...

    @abstractmethod
    def get_entity(self, entity_id: int) -> Entity:
        ...

    @abstractmethod
    def get_singleton_component(self, component: Type[T]) -> T:
        ...

    @abstractmethod
    def create_entity(self, components: list[Component]) -> Entity:
        ...


class IEventBus(ABC):
    @abstractmethod
    def subscribe(self, event_name: str, callback: Callable):
        ...

    @abstractmethod
    def publish(self, event_name: str, **kwargs):
        ...
