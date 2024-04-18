import asyncio

from sqlalchemy import select, delete, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import models
import schemas
from database import async_session


async def create_dish(dish: schemas.DishIn, session: AsyncSession):
    dish_dict = dish.model_dump()
    dish_dict['ingredients'] = []
    for ingredient_sch in dish.ingredients:
        ingredient = await get_ingredient_by_title(session, ingredient_sch.title)
        if ingredient is None:
            ingredient = models.Ingredient(**ingredient_sch.model_dump())
            session.add(ingredient)
            await session.commit()
            await session.refresh(ingredient)
        dish_dict['ingredients'].append(ingredient)
    new_dish = models.Dish(**dish_dict)
    session.add(new_dish)
    await session.commit()
    return new_dish


async def get_ingredient_by_title(session: AsyncSession, title: str):
    stmt = select(models.Ingredient).where(models.Ingredient.title == title)
    ingredient = await session.execute(stmt)
    ingredient = ingredient.scalars().one_or_none()
    return ingredient


async def get_dish_by_title(session: AsyncSession, title: str):
    stmt = select(models.Dish).where(models.Dish.title == title).options(selectinload(models.Dish.ingredients))
    dish = await session.execute(stmt)
    dish = dish.one_or_none()
    return dish


async def get_dish_by_id(session: AsyncSession, dish_id: int, adding_number_views: bool = False):
    stmt = (select(models.Dish)
            .where(models.Dish.id == dish_id)
            .options(selectinload(models.Dish.ingredients)))
    dish = await session.scalars(stmt)
    dish = dish.one_or_none()
    if dish is not None and adding_number_views:
        dish.number_views += 1
        await session.commit()
    return dish


async def update_dish(dish: schemas.DishUpdate, dish_id: int, session: AsyncSession):
    dish_to_update = await get_dish_by_id(session, dish_id)
    if dish_to_update is None:
        return None

    title = dish.title
    if title is not None:
        dish_to_update.title = title

    cooking_time = dish.cooking_time
    if cooking_time is not None:
        dish_to_update.cooking_time = cooking_time

    ingredients: list[schemas.IngredientIn] = dish.ingredients
    if ingredients is not None:
        ingredients_for_update = []
        for ingredient in ingredients:
            ingredient_for_update = await get_ingredient_by_title(session, ingredient.title)
            if ingredient_for_update is None:
                ingredient_for_update = models.Ingredient(**ingredient.model_dump())
            ingredients_for_update.append(ingredient_for_update)
        dish_to_update.ingredients = ingredients_for_update

    description = dish.description
    if description is not None:
        dish_to_update.description = description

    await session.commit()

    return dish_to_update


async def get_dishes(session: AsyncSession):
    stmt = (select(models.Dish)
            .order_by(desc(models.Dish.number_views), models.Dish.cooking_time)
            .options(selectinload(models.Dish.ingredients)))
    dishes = await session.scalars(stmt)
    dishes = dishes.all()
    return dishes


async def del_dish(dish_id: int, session: AsyncSession):
    dish_to_delete = await get_dish_by_id(session, dish_id)
    if dish_to_delete is not None:
        await session.delete(dish_to_delete)
        await session.commit()
        return True
    return False
