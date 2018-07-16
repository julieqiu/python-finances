from typing import List

from recipes.database import db_session
from recipes.models import Recipe


def all_recipes(batch_size: int = 101, category: str=None) -> List[dict]:
    with db_session() as session:
        recipes = session.query(Recipe)
        if category:
            recipes = recipes.filter_by(category=category)

        return [
            dict(
                name=recipe.name,
                url=recipe.url,
                category=recipe.category,
                instructions=recipe.instructions,
                ingredients=recipe.ingredients,
            )
            for recipe in recipes.limit(batch_size).all()
            if recipe.ingredients and recipe.instructions
        ]
