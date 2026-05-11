from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from .associations import recipe_categories, theme_categories

if TYPE_CHECKING:
    from .recipe import Recipe
    from .theme import Theme


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True)

    themes: Mapped[list["Theme"]] = relationship(
        "Theme",
        secondary=theme_categories,
        back_populates="categories",
    )
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe",
        secondary=recipe_categories,
        back_populates="categories",
    )
