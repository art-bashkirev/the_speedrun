from fastapi import FastAPI, status, Header
from models import *
from database import *
from cache_manager import *
from permissions_manager import *

from datetime import datetime

app = FastAPI()

# Auth
@app.post("/auth/login")
async def login(data: LoginModel):
    # TODO: Implement login logic
    return {"message": "Login successful"}

# Admin
@app.get("/admin/cache/clear")
async def clear_cache():
    # TODO: Implement cache clearing logic
    return {"message": "Cache cleared"}


@app.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def create_document(document: DocumentCreate, x_user_id: int = Header(...)):
    new_id = max(fake_documents_db.keys(), default=0) + 1
    new_iso = datetime.now().isoformat()

    document_response = DocumentOut(
        id=new_id,
        title=document.title,
        content=document.content,
        category=document.category,
        is_public=document.is_public,
        created_by=x_user_id,
        created_at=new_iso,
        last_modified=new_iso
    )

    # Database.set_document(new_id, document_response) TODO: ...

    return document_response

@app.put("/documents/{doc_id}")
async def update_document(document: DocumentUpdate, doc_id: int):
    # TODO: ...
    return {"message": f"Document {doc_id} updated"}

@app.post("/documents/{doc_id}/share")
async def share_document(doc_id: int):
    # TODO: ...
    return {"message": f"Document {doc_id} shared"}

@app.delete("/documents/{doc_id}/share")
async def delete_document_share(doc_id: int):
    # TODO: ...
    return {"message": f"Share for document {doc_id} deleted"}
