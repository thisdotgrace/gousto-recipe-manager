
## 📌 Key Principles

- `api/` contains no business logic (only request handling)
- `services/` contains all core logic (filtering, search, transformations)
- `models/` defines database structure
- `schemas/` defines what the API exposes to the frontend
- `ingestion/` handles external data import (e.g. Gousto API sync)
- `db/` handles database connection and configuration


to do in ingestion

- get response from api for key recipe information
- using url slug, get ingredients info
- create rough json object
- transform 



in terms of database

theme table
themecategory table
category table
recipecategory table
ingredients table
recipe ingredients table
