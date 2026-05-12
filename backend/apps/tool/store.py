import uuid
from datetime import datetime, timezone
from typing import List, Optional

from apps.tool.models import ToolCreate, ToolUpdate, ToolResponse

_store: dict[str, dict] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_tool(user_id: str, data: ToolCreate) -> ToolResponse:
    tool_id = str(uuid.uuid4())
    now = _now()
    record = {
        "id": tool_id,
        "user_id": user_id,
        "name": data.name,
        "description": data.description,
        "content": data.content,
        "meta": data.meta,
        "created_at": now,
        "updated_at": now,
    }
    _store[tool_id] = record
    return ToolResponse(**record)


def get_tool(tool_id: str) -> Optional[ToolResponse]:
    record = _store.get(tool_id)
    if record is None:
        return None
    return ToolResponse(**record)


def list_tools_by_user(user_id: str) -> List[ToolResponse]:
    return [
        ToolResponse(**r)
        for r in _store.values()
        if r["user_id"] == user_id
    ]


def update_tool(tool_id: str, data: ToolUpdate) -> Optional[ToolResponse]:
    record = _store.get(tool_id)
    if record is None:
        return None
    updates = data.model_dump(exclude_unset=True)
    record.update(updates)
    record["updated_at"] = _now()
    return ToolResponse(**record)


def delete_tool(tool_id: str) -> bool:
    if tool_id not in _store:
        return False
    del _store[tool_id]
    return True
