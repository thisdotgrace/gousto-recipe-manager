from pydantic import BaseModel
from typing import Optional
from ingredient_parser import parse_ingredient as parse_ing
import re

class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    raw_text: Optional[str] = None

    @staticmethod
    def _extract_multiplier(text: str) -> tuple[str, float]:
        match = re.search(r"\bx(\d+)\b", text, re.I)
        if match:
            text = re.sub(r"\bx\d+\b", "", text, flags=re.I).strip()
            return text, float(match.group(1))

        text = re.sub(r"\bx\b$", "", text, flags=re.I).strip()
        return text, 1.0

    @classmethod
    def parse_ingredient(cls, raw: str) -> "Ingredient":
        raw = raw.replace("†", "").strip()
        clean, mult = cls._extract_multiplier(raw)

        try:
            parsed = parse_ing(clean)

            name = parsed.name[0].text if parsed.name else clean

            quantity, unit = None, None
            if parsed.amount:
                amt = parsed.amount[0]
                quantity = float(amt.quantity) if amt.quantity else None
                unit = str(amt.unit).split(".")[-1].lower() if amt.unit else None

            if quantity is not None:
                quantity *= mult
            elif mult != 1:
                quantity, unit = mult, "pcs"

            return cls(
                name=name.strip().lower(),
                quantity=quantity,
                unit=unit,
                raw_text=raw
            )

        except Exception:
            return cls(
                name=clean,
                quantity=mult if mult != 1 else None,
                unit="pcs" if mult != 1 else None,
                raw_text=raw
            )

    def __str__(self) -> str:
        qty_str = f"{self.quantity} {self.unit}" if self.quantity and self.unit else ""
        return f"{self.name} {qty_str}".strip()