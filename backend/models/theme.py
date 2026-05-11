from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from .associations import theme_categories

if TYPE_CHECKING:
    from .category import Category


class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=theme_categories,
        back_populates="themes",
    )
