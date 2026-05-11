from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from .associations import recipe_ingredients

if TYPE_CHECKING:
    from .recipe import Recipe


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe",
        secondary=recipe_ingredients,
        back_populates="ingredients",
    )
