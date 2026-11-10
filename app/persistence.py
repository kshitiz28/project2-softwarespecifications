from collections.abc import Sequence
from .types import Record, Write

class Persistence:
    def get(self, table: str, key: str) -> Record | None:
        raise NotImplementedError

    def list(self, table: str) -> list[Record]:
        raise NotImplementedError

    def commit(self, writes: Sequence[Write]) -> None:
        raise NotImplementedError
