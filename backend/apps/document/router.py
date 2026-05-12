from fastapi import APIRouter, Depends, HTTPException
from typing import List

from apps.auth.router import get_current_user
from apps.auth.models import UserResponse
from apps.document.models import DocumentCreate, DocumentUpdate, DocumentResponse
from apps.document import store

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentResponse, status_code=201)
def create_document(
    data: DocumentCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    return store.create_document(current_user.id, data)


@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    current_user: UserResponse = Depends(get_current_user),
):
    return store.list_documents_by_user(current_user.id)


@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(
    doc_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    doc = store.get_document(doc_id)
    if not doc or doc.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.put("/{doc_id}", response_model=DocumentResponse)
def update_document(
    doc_id: str,
    data: DocumentUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    doc = store.get_document(doc_id)
    if not doc or doc.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    updated = store.update_document(doc_id, data)
    if not updated:
        raise HTTPException(status_code=500, detail="Update failed")
    return updated


@router.delete("/{doc_id}", status_code=204)
def delete_document(
    doc_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    doc = store.get_document(doc_id)
    if not doc or doc.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    store.delete_document(doc_id)
