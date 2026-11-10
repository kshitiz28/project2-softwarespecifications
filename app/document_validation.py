from .types import Record

class DocumentValidation:
    def validate_document(self, data: bytes, media_type: str, policy: Record) -> None:
        raise NotImplementedError
