from fastapi import APIRouter, Depends, HTTPException, status
from .models import FolderCreate, FolderUpdate, FolderResponse
from . import store
from backend.apps.auth.router import get_current_user

router = APIRouter(prefix="/folders", tags=["folders"])


@router.post("/", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
def create_folder(body: FolderCreate, user=Depends(get_current_user)):
    if body.parent_id:
        parent = store.get_folder(body.parent_id)
        if not parent or parent["user_id"] != user["id"]:
            raise HTTPException(status_code=404, detail="Parent folder not found")
    folder = store.create_folder(user["id"], body.name, body.parent_id)
    return folder


@router.get("/", response_model=list[FolderResponse])
def list_folders(user=Depends(get_current_user)):
    return store.list_folders_by_user(user["id"])


@router.get("/{folder_id}", response_model=FolderResponse)
def get_folder(folder_id: str, user=Depends(get_current_user)):
    folder = store.get_folder(folder_id)
    if not folder or folder["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


@router.patch("/{folder_id}", response_model=FolderResponse)
def update_folder(folder_id: str, body: FolderUpdate, user=Depends(get_current_user)):
    folder = store.get_folder(folder_id)
    if not folder or folder["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Folder not found")
    updated = store.update_folder(folder_id, body.model_dump(exclude_none=True))
    return updated


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(folder_id: str, user=Depends(get_current_user)):
    folder = store.get_folder(folder_id)
    if not folder or folder["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Folder not found")
    store.delete_folder(folder_id)
