from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import models
import schemas


async def create_dish(async_session: async_sessionmaker[AsyncSession], dish: schemas.DishIn):
    async with async_session() as session:
        new_ingredients: list = [models.Ingredient(**ingredient.model_dump()) for ingredient in dish.ingredients]
        session.add_all(new_ingredients)
        await session.commit()
        for ingredient in new_ingredients:
            await session.refresh(ingredient)
        dish_dict = dish.model_dump()
        dish_dict['ingredients'] = new_ingredients
        print(dish.model_dump())
        new_dish = models.Dish(**dish_dict)
        session.add(new_dish)
        await session.commit()
        return new_dish


async def get_dish_by_title(async_session: async_sessionmaker[AsyncSession], title: str):
    async with async_session() as session:
        stmt = select(models.Dish).where(title=title).options(selectinload=models.Dish.ingredients)
        dish = await session.execute(stmt)
        dish.scalars().one()
        return dish
