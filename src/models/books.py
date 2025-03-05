# src/models/books.py
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

class Book(BaseModel):
    __tablename__ = "books_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    pages: Mapped[int] = mapped_column(nullable=False)

    seller_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("sellers_table.id"),
        nullable=True  # позволяем пустое значение
    )
    seller: Mapped["Seller"] = relationship(
        "Seller",
        back_populates="books"
    )
