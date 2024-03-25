from fastapi import FastAPI


from database import engine, session
import models
import schemas


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/dishes', response_model=schemas.DishOut)
async def dishes(dish: schemas.DishIn) -> models.Dish:
    new_ingredients = [models.Ingredient(ingredient.dict()) for ingredient in dish.ingredients]
    dish_dict = dish.dict()
    dish_dict['ingredients'] = new_ingredients
    new_dish = models.Dish(**dish_dict)
    async with session.begin():
        session.add(new_dish)
    return new_dish

