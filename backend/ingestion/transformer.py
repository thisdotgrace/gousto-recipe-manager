import re

def clean_string(value: str) -> str:
    """Normalize a string for lookup/uniqueness.

    Collapse repeated whitespace, strip ends, and lowercase the result.
    """
    return " ".join(value.strip().split()).lower()


def dedupe_list(items: list[str]) -> list[str]:
    """Remove duplicates from a list while preserving order."""
    seen = set()
    deduped = []
    for item in items:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def extract_numeric(value: str) -> float | None:
    """Extract the first numeric value from a string, or return None if not found."""
    match = re.search(r"[\d.]+", value)
    return float(match.group()) if match else None


def mg_to_g(value: float | int | None) -> float | None:
    """Convert milligrams to grams for the macro model fields."""
    if value is None:
        return None
    return float(value) / 1000


def transform_recipe_data(d: dict, slug: str) -> dict:
    """Transform raw recipe data from the API into a normalized format for loading."""
    nutritional_info = d.get("nutritional_information", {}).get("per_portion", {})
    images = d.get("media", {}).get("images", [])

    return {
        "gousto_id": d["gousto_id"],
        "title": " ".join(d["title"].split()),
        "slug": slug,
        "image_url": images[1]["image"] if len(images) > 1 else None,
        "cuisine": clean_string(d["cuisine"]["title"]) if d.get("cuisine") else None,
        "ingredients": dedupe_list([clean_string(i["name"]) for i in d.get("ingredients", [])]),
        "categories": [],
        "macros": {
            "kcal": nutritional_info.get("energy_kcal"),
            "fat_g": mg_to_g(nutritional_info.get("fat_mg")),
            "saturates_g": mg_to_g(nutritional_info.get("fat_saturates_mg")),
            "carbs_g": mg_to_g(nutritional_info.get("carbs_mg")),
            "sugars_g": mg_to_g(nutritional_info.get("carbs_sugars_mg")),
            "protein_g": mg_to_g(nutritional_info.get("protein_mg")),
            "fibre_g": mg_to_g(nutritional_info.get("fibre_mg")),
            "salt_g": mg_to_g(nutritional_info.get("salt_mg")),
        }
    }

def transform_theme_data(d: dict) -> dict:
    """Transform raw theme data from the API into a normalized format for loading."""
    return {
        "title": clean_string(d["title"]),
        "categories": dedupe_list(
            [clean_string(c["url"].split("/")[-1]) for c in d.get("categories", [])]
        )
    }