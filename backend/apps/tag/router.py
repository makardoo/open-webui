from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from apps.auth.router import get_current_user
from apps.auth.models import UserResponse
from apps.tag.models import TagCreate, TagUpdate, TagResponse
from apps.tag import store

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    data: TagCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.create_tag(user_id=current_user.id, data=data)


@router.get("/", response_model=List[TagResponse])
def list_tags(
    current_user: UserResponse = Depends(get_current_user),
):
    return store.list_tags_by_user(user_id=current_user.id)


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    tag = store.get_tag(tag_id)
    if tag is None or tag.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: str,
    data: TagUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    tag = store.get_tag(tag_id)
    if tag is None or tag.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    updated = store.update_tag(tag_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    tag = store.get_tag(tag_id)
    if tag is None or tag.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    store.delete_tag(tag_id)
