from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, List


# Регистрация пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8) = Field(..., description="Password, at least 8 characters")


# Логин пользователя
class LoginModel(BaseModel):
    username: str
    password: str


# Создание документа
class DocumentCreate(BaseModel):
    title: str
    content: str
    is_public: bool
    category: str


# Обновление документа
class DocumentUpdate(BaseModel):
    id: int
    title: Optional[str]
    content: Optional[str]
    is_public: Optional[bool]
    category: Optional[str]


# Отправляем один документ
class DocumentOut(BaseModel):
    id: int
    title: str
    content: str
    is_public: bool
    category: str
    created_by: int
    created_at: str
    last_modified: str


# Отправляем несколько документов
class ManyDocumentsOut(BaseModel):
    documents: List[DocumentOut]
