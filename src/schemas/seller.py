from pydantic import BaseModel
from typing import Optional

# Схема для регистрации нового продавца
class IncomingSeller(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True

# Схема для возврата данных о продавце (без пароля)
class ReturnedSeller(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

# Схема для обновления данных продавца (без изменения книг и пароля)
class IncomingSellerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True

# Схема для книги в контексте продавца – возвращаем поле count_pages вместо pages
class SellerBook(BaseModel):
    id: int
    title: str
    author: str
    year: int
    count_pages: int

    class Config:
        orm_mode = True

# Схема для детального представления продавца с его книгами
class ReturnedSellerWithBooks(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    books: list[SellerBook] = []

    class Config:
        orm_mode = True
