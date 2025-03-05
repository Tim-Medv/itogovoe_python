from typing import Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllbooks"]

class BaseBook(BaseModel):
    title: str
    author: str
    year: int

class IncomingBook(BaseBook):
    pages: int = Field(default=150, alias="count_pages")
    seller_id: Optional[int] = None

    @field_validator("year")
    @staticmethod
    def validate_year(val: int):
        if val < 2020:
            raise PydanticCustomError("Validation error", "Year is too old!")
        return val

class ReturnedBook(BaseBook):
    id: int
    pages: int
    seller_id: Optional[int] = None

    class Config:
        orm_mode = True
        exclude_none = True  # если seller_id равен None, поле не будет включено в ответ

class ReturnedAllbooks(BaseModel):
    books: list[ReturnedBook]

    class Config:
        orm_mode = True
        exclude_none = True
