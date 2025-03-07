from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel

class Seller(BaseModel):
    __tablename__ = "sellers_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="seller",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    @property
    def email(self) -> str:
        return self.e_mail