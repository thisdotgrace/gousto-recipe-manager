from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from .associations import recipe_categories, recipe_ingredients

if TYPE_CHECKING:
    from .category import Category
    from .cuisine import Cuisine
    from .ingredient import Ingredient
    from .macros import RecipeMacros


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    gousto_id: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True)

    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    cuisine_id: Mapped[int | None] = mapped_column(
        ForeignKey("cuisines.id"), nullable=True
    )

    cuisine: Mapped["Cuisine | None"] = relationship(
        "Cuisine", back_populates="recipes"
    )
    macros: Mapped["RecipeMacros | None"] = relationship(
        "RecipeMacros", back_populates="recipe", uselist=False
    )
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=recipe_categories,
        back_populates="recipes",
    )
    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient",
        secondary=recipe_ingredients,
        back_populates="recipes",
    )
