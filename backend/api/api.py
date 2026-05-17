from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload


from api.dependencies import get_db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient

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
        .options(joinedload(Recipe.cuisine), joinedload(Recipe.macros))
        .offset(offset)
        .limit(limit)
        .all()
    )

    data = [
        {
            "id": r.id,
            "title": r.title,
            "slug": r.slug,
            "image_url": r.image_url,
            "prep_time": r.prep_time,
            "rating": (
                {"average": r.rating_average, "count": r.rating_count}
                if r.rating_average is not None
                else None
            ),
            "cuisine": r.cuisine.name if r.cuisine else None,
            "calories": r.macros.energy_kcal if r.macros else None,
        }
        for r in recipes
    ]

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

    return {
        "id": recipe.id,
        "title": recipe.title,
        "slug": recipe.slug,
        "prep_time": recipe.prep_time,
        "rating": (
            {"average": recipe.rating_average, "count": recipe.rating_count}
            if recipe.rating_average is not None
            else None
        ),
        "image_url": recipe.image_url,
        "cuisine": recipe.cuisine.name if recipe.cuisine else None,
        "macros": (
            {
                "energy_kcal": recipe.macros.energy_kcal,
                "protein_g": recipe.macros.protein_g,
                "fat_g": recipe.macros.fat_g,
                "carbs_g": recipe.macros.carbs_g,
            }
            if recipe.macros
            else None
        ),
        "categories": [c.slug for c in recipe.categories],
        "ingredients": [i.name for i in recipe.ingredients],
    }


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
