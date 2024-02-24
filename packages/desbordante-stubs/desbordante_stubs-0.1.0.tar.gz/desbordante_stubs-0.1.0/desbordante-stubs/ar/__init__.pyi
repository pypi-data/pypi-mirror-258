from __future__ import annotations
import desbordante
from . import algorithms

__all__ = ["ArAlgorithm", "AssociativeRule", "algorithms"]

class ArAlgorithm(desbordante.Algorithm):
    def get_ars(self) -> list[AssociativeRule]: ...

class AssociativeRule:
    def __str__(self) -> str: ...
    @property
    def confidence(self) -> float: ...
    @property
    def left(self) -> list[str]: ...
    @property
    def right(self) -> list[str]: ...
