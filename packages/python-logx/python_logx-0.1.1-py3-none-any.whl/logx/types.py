from __future__ import annotations

from typing_extensions import (
    Any,
    Protocol,
    TypeVar,
    overload,
    runtime_checkable,
)

T = TypeVar("T", covariant=True)


@runtime_checkable
class WithFactory(Protocol[T]):
    def new(self, config: dict, namespace: dict, converter: Converter) -> T:
        ...


class Converter(Protocol):
    @overload
    def convert(self, value: dict, namespace: dict) -> dict:
        ...

    @overload
    def convert(self, value: tuple, namespace: dict) -> tuple:
        ...

    @overload
    def convert(self, value: dict, namespace: dict) -> dict:
        ...

    @overload
    def convert(self, value: Any, namespace: dict) -> Any:
        ...
