import time
import uuid
from typing import List, Optional

from apps.document.models import DocumentCreate, DocumentUpdate, DocumentResponse

_documents: dict = {}


def _now() -> int:
    return int(time.time())


def create_document(user_id: str, data: DocumentCreate) -> DocumentResponse:
    doc_id = str(uuid.uuid4())
    now = _now()
    doc = {
        "id": doc_id,
        "user_id": user_id,
        "title": data.title,
        "content": data.content,
        "collection_name": data.collection_name,
        "created_at": now,
        "updated_at": now,
    }
    _documents[doc_id] = doc
    return DocumentResponse(**doc)


def get_document(doc_id: str) -> Optional[DocumentResponse]:
    doc = _documents.get(doc_id)
    return DocumentResponse(**doc) if doc else None


def list_documents_by_user(user_id: str) -> List[DocumentResponse]:
    return [
        DocumentResponse(**d)
        for d in _documents.values()
        if d["user_id"] == user_id
    ]


def update_document(doc_id: str, data: DocumentUpdate) -> Optional[DocumentResponse]:
    doc = _documents.get(doc_id)
    if not doc:
        return None
    updates = data.dict(exclude_unset=True)
    doc.update(updates)
    doc["updated_at"] = _now()
    _documents[doc_id] = doc
    return DocumentResponse(**doc)


def delete_document(doc_id: str) -> bool:
    if doc_id in _documents:
        del _documents[doc_id]
        return True
    return False
