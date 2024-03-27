import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import models
import schemas


async def create_dish(async_session, dish: schemas.DishIn):
    async with async_session() as session:
        new_ingredients = await create_ingredients(async_session, dish.ingredients)
        dish_dict = dish.model_dump()
        dish_dict['ingredients'] = new_ingredients
        new_dish = models.Dish(**dish_dict)
        session.add(new_dish)
        await session.commit()
        return new_dish


async def create_ingredients(async_session, ingredients: list[schemas.IngredientIn]):
    ingredients = [create_ingredient(async_session, ingredient) for ingredient in ingredients]
    return await asyncio.gather(*ingredients)


async def create_ingredient(async_session, ingredient: schemas.IngredientIn):
    async with async_session() as session:
        new_ingredient = models.Ingredient(**ingredient.model_dump())
        session.add(new_ingredient)
        await session.commit()
        await session.refresh(new_ingredient)
        return new_ingredient


async def get_dish_by_title(session: AsyncSession, title: str):
    stmt = select(models.Dish).where(models.Dish.title == title).options(selectinload(models.Dish.ingredients))
    dish = await session.scalars(stmt)
    dish = dish.one_or_none()
    return dish


async def get_dish_by_id(session: AsyncSession, dish_id: int):
    stmt = select(models.Dish).where(id=dish_id)
    dish = await session.scalars(stmt)
    dish = dish.one_or_none()
    dish.number_views += 1
    await session.commit()
    return dish


async def update_dish(dish: schemas.DishUpdate, dish_id: int, session: AsyncSession):
    stmt = select(models.Dish).where(id=dish_id)
    dish_to_update = await session.scalars(stmt)
    dish_to_update = dish.one()
    dish_dict = dish.model_dump()

    title = dish_dict.pop('title', False)
    if title:
        dish_to_update.title = title

    cooking_time = dish_dict.pop('cooking_time', False)
    if cooking_time:
        dish_to_update.cooking_time = cooking_time


async def get_dishes(session: AsyncSession):
    stmt = select(models.Dish).order_by(desc(models.Dish.number_views), models.Dish.cooking_time)
    dishes = await session.scalars(stmt)
    dishes = dishes.all()
    return dishes
