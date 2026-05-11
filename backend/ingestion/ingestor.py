import requests
from time import sleep
from .loader import load_recipe, load_themes
from db.session import SessionLocal, engine
from db.base import Base
from .api import fetch_themes, fetch_categories, fetch_all_recipes_for_category, fetch_recipe_details

GOUSTO_API_URL = "https://production-api.gousto.co.uk/cmsreadbroker/v1/"

REQUEST_DELAY = 0.1 

def ingest_all(session):

    themes = fetch_themes()
    categories = fetch_categories(themes)

    metrics = {
        "themes": len(themes),
        "categories": len(categories),
        "recipes_processed": 0,
        "failed_recipes": 0,
        "duplicates_estimated": 0
    }

    with session:

        load_themes(session, themes)

        for category in categories:
            recipes = fetch_all_recipes_for_category(category)

            for recipe in recipes:
                try:
                    slug = recipe["url"].split("/")[-1]
                    recipe_data = fetch_recipe_details(slug)
                    recipe_data["categories"] = [category]
                    load_recipe(session, recipe_data)
                    metrics["recipes_processed"] += 1
                    sleep(REQUEST_DELAY)

                except requests.RequestException as e:
                    print(f"Failed to fetch {recipe['slug']}: {e}")
                    metrics['failed_recipes'] += 1
        
        session.commit()
        print("\n=== INGESTION SUMMARY ===")
        print(f"Themes: {metrics['themes']}")
        print(f"Categories: {metrics['categories']}")
        print(f"Recipes processed: {metrics['recipes_processed']}")
        print(f"Failed recipe fetches: {metrics['failed_recipes']}")

          
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    ingest_all(SessionLocal())