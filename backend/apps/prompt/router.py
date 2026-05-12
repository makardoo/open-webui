from fastapi import APIRouter, Depends, HTTPException, status

from apps.auth.router import get_current_user
from apps.auth.models import UserResponse
from apps.prompt.models import PromptCreate, PromptUpdate, PromptResponse
from apps.prompt import store

router = APIRouter(prefix="/prompts", tags=["prompts"])


@router.post("/", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
def create_prompt(
    data: PromptCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.create_prompt(user_id=current_user.id, data=data)


@router.get("/", response_model=list[PromptResponse])
def list_prompts(
    current_user: UserResponse = Depends(get_current_user),
):
    return store.list_prompts_by_user(user_id=current_user.id)


@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(
    prompt_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    prompt = store.get_prompt(prompt_id)
    if prompt is None or prompt.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return prompt


@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt(
    prompt_id: str,
    data: PromptUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    existing = store.get_prompt(prompt_id)
    if existing is None or existing.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    updated = store.update_prompt(prompt_id, data)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    return updated


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prompt(
    prompt_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    existing = store.get_prompt(prompt_id)
    if existing is None or existing.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
    store.delete_prompt(prompt_id)
