from .types import Record

class SchedulingAdapter:
    def request(self, operation: str, payload: Record, timeout_seconds: int) -> Record:
        raise NotImplementedError
