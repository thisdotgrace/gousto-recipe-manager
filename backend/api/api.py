from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, selectinload


from api.dependencies import get_db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient


def serialize_macros(macros):
    if not macros:
        return None

    return {
        "energy_kcal": macros.energy_kcal,
        "protein_g": macros.protein_g,
        "fat_g": macros.fat_g,
        "saturates_g": macros.saturates_g,
        "carbs_g": macros.carbs_g,
        "sugars_g": macros.sugars_g,
        "fibre_g": macros.fibre_g,
        "salt_g": macros.salt_g,
    }


def serialize_recipe(recipe):
    categories = list(recipe.categories or [])
    themes = []
    seen_theme_titles = set()

    for category in categories:
        for theme in category.themes or []:
            if theme.title not in seen_theme_titles:
                seen_theme_titles.add(theme.title)
                themes.append(theme.title)

    return {
        "id": recipe.id,
        "title": recipe.title,
        "slug": recipe.slug,
        "image_url": recipe.image_url,
        "prep_time": recipe.prep_time,
        "rating": (
            {"average": recipe.rating_average, "count": recipe.rating_count}
            if recipe.rating_average is not None
            else None
        ),
        "cuisine": recipe.cuisine.name if recipe.cuisine else None,
        "calories": recipe.macros.energy_kcal if recipe.macros else None,
        "macros": serialize_macros(recipe.macros),
        "ingredients": [ingredient.name for ingredient in recipe.ingredients or []],
        "categories": [category.slug for category in categories],
        "themes": themes,
    }


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    import traceback

    try:
        from sqlalchemy import text
        from db.session import SessionLocal

        db = SessionLocal()
        total = db.execute(text("SELECT count(*) FROM recipes")).scalar()
        return {"message": "Hello World", "db_count": total}
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}


@app.get("/recipes")
async def get_recipes(
    offset: int = Query(0, description="Skip the first N recipes"),
    limit: int = Query(50, description="Limit the number of recipes returned", le=100),
    db: Session = Depends(get_db),
):

    total = db.query(Recipe).count()
    recipes = (
        db.query(Recipe)
        .options(
            selectinload(Recipe.cuisine),
            selectinload(Recipe.macros),
            selectinload(Recipe.ingredients),
            selectinload(Recipe.categories).selectinload(Category.themes),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    data = [serialize_recipe(recipe) for recipe in recipes]

    return {"total": total, "offset": offset, "limit": limit, "data": data}


@app.get("/recipes/autocomplete")
async def autocomplete_recipes(
    q: str = Query(..., min_length=1, description="Search query for autocomplete"),
    offset: int = Query(0, description="Skip the first N recipes"),
    limit: int = Query(10, description="Max number of suggestions to return", le=100),
    db: Session = Depends(get_db),
):
    """
    Returns lightweight search suggestions based on the recipe title.
    """
    # Use ilike for case-insensitive partial matching
    recipes = (
        db.query(Recipe)
        .filter(Recipe.title.ilike(f"%{q}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Recipe).filter(Recipe.title.ilike(f"%{q}%")).count()

    data = [
        {"id": recipe.id, "title": recipe.title, "slug": recipe.slug}
        for recipe in recipes
    ]

    return {"total": total, "offset": offset, "limit": limit, "data": data}


@app.get("/recipes/cuisines")
async def get_cuisines(db: Session = Depends(get_db)):
    from models.cuisine import Cuisine

    cuisines = db.query(Cuisine).all()
    return {"cuisines": cuisines}


@app.get("/recipes/{slug}")
async def get_recipe(slug: str, db: Session = Depends(get_db)):
    """Fetch full recipe details including macros, ingredients, and cuisine."""
    recipe = (
        db.query(Recipe)
        .options(
            selectinload(Recipe.ingredients),
            selectinload(Recipe.macros),
            selectinload(Recipe.cuisine),
            selectinload(Recipe.categories).selectinload(Category.themes),
        )
        .filter(Recipe.slug == slug)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return serialize_recipe(recipe)


@app.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """List all recipe categories."""
    return db.query(Category).all()


@app.get("/categories/autocomplete")
async def autocomplete_categories(
    q: str = Query(..., min_length=1, description="Search query for autocomplete"),
    limit: int = Query(10, description="Max number of suggestions to return", le=100),
    db: Session = Depends(get_db),
):
    """
    Returns lightweight search suggestions based on the category slug.
    """
    categories = (
        db.query(Category).filter(Category.slug.ilike(f"%{q}%")).limit(limit).all()
    )

    return [{"id": category.id, "slug": category.slug} for category in categories]


@app.get("/ingredients/{ingredient_id}/recipes")
async def get_recipes_by_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Find all recipes that use a specific ingredient."""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    return ingredient.recipes
