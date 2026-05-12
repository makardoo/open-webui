import time
import uuid
from typing import Optional

_folders: dict = {}


def _now() -> int:
    return int(time.time())


def create_folder(user_id: str, name: str, parent_id: Optional[str] = None) -> dict:
    folder_id = str(uuid.uuid4())
    folder = {
        "id": folder_id,
        "user_id": user_id,
        "name": name,
        "parent_id": parent_id,
        "created_at": _now(),
        "updated_at": _now(),
    }
    _folders[folder_id] = folder
    return folder


def get_folder(folder_id: str) -> Optional[dict]:
    return _folders.get(folder_id)


def list_folders_by_user(user_id: str) -> list:
    return [f for f in _folders.values() if f["user_id"] == user_id]


def update_folder(folder_id: str, updates: dict) -> Optional[dict]:
    folder = _folders.get(folder_id)
    if not folder:
        return None
    folder.update({k: v for k, v in updates.items() if v is not None})
    folder["updated_at"] = _now()
    return folder


def delete_folder(folder_id: str) -> bool:
    if folder_id in _folders:
        del _folders[folder_id]
        return True
    return False


def clear_all() -> None:
    _folders.clear()
