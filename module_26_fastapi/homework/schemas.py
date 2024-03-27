from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    cooking_time: int
    description: str


class DishIn(BaseDish):
    ingredients: list['IngredientIn']


class DishOut(BaseDish):
    id: int
    ingredients: list['IngredientOut']
    number_views: int


class DishUpdate(BaseModel):
    title: str = None
    cooking_time: int = None
    ingredients: list['IngredientIn']


class BaseIngredient(BaseModel):
    title: str


class IngredientIn(BaseIngredient):
    ...


class IngredientOut(BaseIngredient):
    id: int
