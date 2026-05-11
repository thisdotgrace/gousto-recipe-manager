import requests

from ingestion.transformer import transform_recipe_data, transform_theme_data

GOUSTO_API_URL = "https://production-api.gousto.co.uk/cmsreadbroker/v1/"


def get_response(endpoint):
    """Helper to make GET requests to the Gousto API and return JSON data."""
    response = requests.get(f"{GOUSTO_API_URL}{endpoint}")
    response.raise_for_status()
    return response.json()


def fetch_themes():
    """Fetches themes from the API and transforms them for loading."""
    response = get_response("themes")
    themes = response["data"]["entries"]
    return [transform_theme_data(theme) for theme in themes]


def fetch_categories(themes):
    """Extracts unique category slugs from the list of themes."""
    return sorted({c for t in themes for c in t.get("categories", [])})


def fetch_all_recipes_for_category(category, limit=60, max_pages=50):
    """Fetches all recipes for a given category, handling pagination."""
    all_recipes = []

    for page in range(max_pages):
        offset = page * limit

        response = get_response(
            f"recipes?category={category}&limit={limit}&offset={offset}"
        )
        batch = response["data"]["entries"]
        all_recipes.extend(batch)

        print(f"{category}: fetched {len(batch)} (page {page})")

        if len(batch) < limit:
            break

    return all_recipes


def fetch_recipe_details(slug):
    """Fetches detailed recipe data for a given slug and transforms it for loading."""
    response = get_response(f"recipe/{slug}")
    raw_recipe = response["data"]["entry"]

    return transform_recipe_data(raw_recipe, slug)
