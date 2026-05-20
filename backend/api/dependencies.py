from db.session import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_api_base_url():
    """Dependency to provide the canonical recipe base URL.

    Can be overridden in tests or via environment wiring in future.
    """
    from os import getenv

    yield getenv("RECIPE_BASE_URL", "https://www.gousto.co.uk")
