from pydantic import BaseModel


class BaseDish(BaseModel):
    title: str
    cooking_time: int


class DishIn(BaseDish):
    ingredients: list['IngredientIn']
    description: str


class DishOutReadDishes(BaseDish):
    id: int
    number_views: int


class DishOutReadDish(BaseDish):
    id: int
    ingredients: list['IngredientOut']
    description: str


class DishOutCreateDish(BaseDish):
    id: int
    ingredients: list['IngredientOut']
    description: str
    number_views: int


class DishUpdate(BaseModel):
    title: str = None
    cooking_time: int = None
    ingredients: list['IngredientIn'] = None
    description: str = None


class BaseIngredient(BaseModel):
    title: str


class IngredientIn(BaseIngredient):
    ...


class IngredientOut(BaseIngredient):
    id: int
