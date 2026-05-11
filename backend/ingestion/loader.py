from sqlalchemy.orm import Session

from models import Recipe, Cuisine, Ingredient, Category, RecipeMacros
from models.theme import Theme


def get_or_create(session: Session, model, defaults=None, **kwargs):
    """Generic get-or-create helper for SQLAlchemy models."""
    obj = session.query(model).filter_by(**kwargs).first()
    if obj:
        return obj

    params = {**kwargs, **(defaults or {})}
    obj = model(**params)
    session.add(obj)
    session.flush()  # ensures obj gets an ID without full commit
    return obj


def load_recipe(session: Session, data: dict):
    """
    Loads a single transformed recipe into the database.
    Assumes `data` is CLEAN (output of transformer.py).
    """

    cuisine = None
    if data.get("cuisine"):
        cuisine = get_or_create(session, Cuisine, name=data["cuisine"])

    recipe = get_or_create(
        session,
        Recipe,
        gousto_id=data["gousto_id"],
        slug=data["slug"],
        defaults={
            "title": data["title"],
            "image_url": data.get("image_url"),
        },
    )

    # attach cuisine (safe even if already exists)
    recipe.cuisine = cuisine

    ingredients = []
    for name in data.get("ingredients", []):
        ingredient = get_or_create(session, Ingredient, name=name)
        ingredients.append(ingredient)

    recipe.ingredients = ingredients

    categories = []
    for slug in data.get("categories", []):
        category = get_or_create(session, Category, slug=slug)
        categories.append(category)

    recipe.categories = categories

    macros_data = data.get("macros")

    if macros_data:

        if not recipe.macros:
            recipe.macros = RecipeMacros()

        recipe.macros.energy_kcal = macros_data.get("kcal")
        recipe.macros.protein_g = macros_data.get("protein_g")
        recipe.macros.fat_g = macros_data.get("fat_g")
        recipe.macros.saturates_g = macros_data.get("saturates_g")
        recipe.macros.carbs_g = macros_data.get("carbs_g")
        recipe.macros.sugars_g = macros_data.get("sugars_g")
        recipe.macros.fibre_g = macros_data.get("fibre_g")
        recipe.macros.salt_g = macros_data.get("salt_g")

    return recipe


def load_themes(session: Session, themes: list[dict]):
    """Loads themes and their associated categories into the database."""
    for theme_data in themes:
        theme = get_or_create(session, Theme, title=theme_data["title"])

        categories = []

        for slug in theme_data.get("categories", []):
            category = get_or_create(session, Category, slug=slug)
            categories.append(category)

        theme.categories = categories
