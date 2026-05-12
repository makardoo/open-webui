from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from apps.auth.router import get_current_user
from apps.auth.models import UserResponse
from apps.tool.models import ToolCreate, ToolUpdate, ToolResponse
import apps.tool.store as store

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
def create_tool(
    data: ToolCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.create_tool(user_id=current_user.id, data=data)


@router.get("/", response_model=List[ToolResponse])
def list_tools(
    current_user: UserResponse = Depends(get_current_user),
):
    return store.list_tools_by_user(user_id=current_user.id)


@router.get("/{tool_id}", response_model=ToolResponse)
def get_tool(
    tool_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    tool = store.get_tool(tool_id)
    if tool is None or tool.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return tool


@router.patch("/{tool_id}", response_model=ToolResponse)
def update_tool(
    tool_id: str,
    data: ToolUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    existing = store.get_tool(tool_id)
    if existing is None or existing.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    updated = store.update_tool(tool_id, data)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return updated


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool(
    tool_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    existing = store.get_tool(tool_id)
    if existing is None or existing.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    store.delete_tool(tool_id)
