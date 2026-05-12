import uuid
from datetime import datetime, timezone
from typing import List, Optional

from apps.tag.models import TagCreate, TagUpdate, TagResponse

_tags: dict[str, dict] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_tag(user_id: str, data: TagCreate) -> TagResponse:
    tag_id = str(uuid.uuid4())
    now = _now()
    record = {
        "id": tag_id,
        "user_id": user_id,
        "name": data.name,
        "color": data.color,
        "created_at": now,
        "updated_at": now,
    }
    _tags[tag_id] = record
    return TagResponse(**record)


def get_tag(tag_id: str) -> Optional[TagResponse]:
    record = _tags.get(tag_id)
    if record is None:
        return None
    return TagResponse(**record)


def list_tags_by_user(user_id: str) -> List[TagResponse]:
    return [
        TagResponse(**r)
        for r in _tags.values()
        if r["user_id"] == user_id
    ]


def update_tag(tag_id: str, data: TagUpdate) -> Optional[TagResponse]:
    record = _tags.get(tag_id)
    if record is None:
        return None
    if data.name is not None:
        record["name"] = data.name
    if data.color is not None:
        record["color"] = data.color
    record["updated_at"] = _now()
    return TagResponse(**record)


def delete_tag(tag_id: str) -> bool:
    if tag_id not in _tags:
        return False
    del _tags[tag_id]
    return True
