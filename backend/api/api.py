from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dependencies import get_db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/recipes")
async def get_recipes(
    offset: int = Query(0, description="Skip the first N recipes"),
    limit: int = Query(50, description="Limit the number of recipes returned", le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Recipe).count()
    recipes = db.query(Recipe).offset(offset).limit(limit).all()

    return {"total": total, "offset": offset, "limit": limit, "data": recipes}


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


@app.get("/recipes/{slug}")
async def get_recipe(slug: str, db: Session = Depends(get_db)):
    """Fetch full recipe details including macros, ingredients, and cuisine."""
    from sqlalchemy.orm import joinedload

    # joinedload eagerly loads the related tables so you don't hit the N+1 queries problem
    recipe = (
        db.query(Recipe)
        .options(
            joinedload(Recipe.ingredients),
            joinedload(Recipe.macros),
            joinedload(Recipe.cuisine),
            joinedload(Recipe.categories),
        )
        .filter(Recipe.slug == slug)
        .first()
    )

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.get("/recipes/cuisines")
async def get_cuisines(db: Session = Depends(get_db)):
    cuisines = db.query(Recipe.cuisine).distinct().all()
    return {"cuisines": cuisines}


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
