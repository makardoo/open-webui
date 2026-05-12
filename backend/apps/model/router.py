from fastapi import APIRouter, Depends, HTTPException, status

from backend.apps.auth.router import get_current_user
from backend.apps.model.models import ModelCreate, ModelUpdate, ModelResponse
from backend.apps.model import store

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
def create_model(
    payload: ModelCreate,
    current_user=Depends(get_current_user),
):
    record = store.create_model(current_user["id"], payload.model_dump())
    return record


@router.get("/", response_model=list[ModelResponse])
def list_models(current_user=Depends(get_current_user)):
    return store.list_models_by_user(current_user["id"])


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: str,
    current_user=Depends(get_current_user),
):
    record = store.get_model(model_id)
    if not record or record["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Model not found")
    return record


@router.patch("/{model_id}", response_model=ModelResponse)
def update_model(
    model_id: str,
    payload: ModelUpdate,
    current_user=Depends(get_current_user),
):
    record = store.get_model(model_id)
    if not record or record["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Model not found")
    updated = store.update_model(model_id, payload.model_dump(exclude_unset=True))
    return updated


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(
    model_id: str,
    current_user=Depends(get_current_user),
):
    record = store.get_model(model_id)
    if not record or record["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Model not found")
    store.delete_model(model_id)
