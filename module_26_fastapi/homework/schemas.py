from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    cooking_time: int
    number_views: int


class DishIn(BaseDish):
    ingredients: list['IngredientIn']


class DishOut(BaseDish):
    id: int
    ingredients: list['IngredientOut']


class BaseIngredient(BaseModel):
    title: str


class IngredientIn(BaseIngredient):
    ...


class IngredientOut(BaseIngredient):
    id: int
