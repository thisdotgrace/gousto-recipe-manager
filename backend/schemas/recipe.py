from pydantic import BaseModel
from typing import Optional

from .ingredient import Ingredient


class Rating(BaseModel):
    average: Optional[float] = None
    count: Optional[int] = None


class Recipe(BaseModel):
    title: str
    url: str
    image_url: Optional[str] = None
    reviews: Optional[int] = None
    rating: Optional[Rating] = None
    calories: Optional[int] = None  # per serving
    time: Optional[int] = None
    prep_time: Optional[int] = None
    cuisine: Optional[str] = None
    ingredients: Optional[list[Ingredient]] = None

    def __str__(self) -> str:
        return (
            f"{self.title}\n"
            f"{'-' * len(self.title)}\n"
            f"Cuisine: {self.cuisine or 'N/A'}\n"
            f"Time: {self.time or 'N/A'} mins\n"
            f"Prep Time: {self.prep_time or 'N/A'} mins\n"
            f"Calories: {self.calories or 'N/A'} kcal\n"
            f"Rating: {self.rating.average if self.rating else 'N/A'} ({self.rating.count if self.rating else 0} reviews)\n"
            f"URL: {self.url}\n"
            f"Ingredients:\n"
            + "\n".join(f"  - {ing}" for ing in (self.ingredients or []))
        )
