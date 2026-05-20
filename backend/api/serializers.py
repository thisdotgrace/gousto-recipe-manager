from typing import Any, Dict, List


def serialize_macros(macros: Any) -> Dict[str, Any] | None:
    if not macros:
        return None

    return {
        "energy_kcal": getattr(macros, "energy_kcal", None),
        "protein_g": getattr(macros, "protein_g", None),
        "fat_g": getattr(macros, "fat_g", None),
        "saturates_g": getattr(macros, "saturates_g", None),
        "carbs_g": getattr(macros, "carbs_g", None),
        "sugars_g": getattr(macros, "sugars_g", None),
        "fibre_g": getattr(macros, "fibre_g", None),
        "salt_g": getattr(macros, "salt_g", None),
    }


def serialize_recipe(recipe: Any, base_url: str | None = None) -> Dict[str, Any]:
    """Serialize a Recipe ORM object into a JSON-friendly dict.

    `base_url` is optional; when provided it will be used to build an absolute
    `url` field on the returned object. This keeps URL composition out of
    presentation code and makes it easy to change the host in one place.
    """
    categories: List[Any] = list(recipe.categories or [])
    themes: List[str] = []
    seen_theme_titles = set()

    for category in categories:
        for theme in category.themes or []:
            if getattr(theme, "title", None) and theme.title not in seen_theme_titles:
                seen_theme_titles.add(theme.title)
                themes.append(theme.title)

    slug = getattr(recipe, "slug", None)
    url = None
    if base_url and slug:
        url = f"{base_url.rstrip('/')}/cookbook/recipes/{slug}"

    return {
        "id": getattr(recipe, "id", None),
        "title": getattr(recipe, "title", None),
        "slug": slug,
        "url": url,
        "image_url": getattr(recipe, "image_url", None),
        "prep_time": getattr(recipe, "prep_time", None),
        "rating": (
            {
                "average": getattr(recipe, "rating_average", None),
                "count": getattr(recipe, "rating_count", None),
            }
            if getattr(recipe, "rating_average", None) is not None
            else None
        ),
        "cuisine": (
            getattr(getattr(recipe, "cuisine", None), "name", None)
            if getattr(recipe, "cuisine", None)
            else None
        ),
        "calories": (
            getattr(getattr(recipe, "macros", None), "energy_kcal", None)
            if getattr(recipe, "macros", None)
            else None
        ),
        "macros": serialize_macros(getattr(recipe, "macros", None)),
        "ingredients": [
            getattr(i, "name", None)
            for i in (getattr(recipe, "ingredients", None) or [])
        ],
        "categories": [getattr(c, "slug", None) for c in categories],
        "themes": themes,
    }
