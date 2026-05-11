from sqlalchemy import Column, ForeignKey, Table

from db.base import Base


recipe_categories = Table(
    "recipe_categories",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)

recipe_ingredients = Table(
    "recipe_ingredients",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
)

theme_categories = Table(
    "theme_categories",
    Base.metadata,
    Column("theme_id", ForeignKey("themes.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)
