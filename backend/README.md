
## 📌 Key Principles

- `api/` contains no business logic (only request handling)
- `services/` contains all core logic (filtering, search, transformations)
- `models/` defines database structure
- `schemas/` defines what the API exposes to the frontend
- `ingestion/` handles external data import (e.g. Gousto API sync)
- `db/` handles database connection and configuration


## Project Status

-   **Database Models Defined:** Created SQLAlchemy tables for Themes, Categories, Recipes, Ingredients, and Macros with proper relationships.
-   **Ingestion Pipeline Configured:** Built a fully functional ETL script that pulls real data from Gousto's production CMS API.
-   **Idempotent Data Loading:** Implemented `get_or_create` logic to safely insert and link recipes without duplicating cuisines or ingredients.
-   **Schema Prepared:** Added Pydantic schemas to structure data for the planned FastAPI endpoints.
-   **Environment Setup:** Configured `pyproject.toml` with `fastapi`, `sqlalchemy`, `pydantic`, and `ruff`.

- pre-commit run --all-files


* ingestion
* transformation
* persistence
