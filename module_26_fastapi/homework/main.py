from fastapi import FastAPI, HTTPException
import uvicorn


from database import engine, async_session
from crud import create_dish, get_dish_by_title, models, schemas


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.post('/dishes', response_model=schemas.DishOut)
async def dishes(dish: schemas.DishIn) -> models.Dish:
    db_dish = get_dish_by_title(async_session, dish.title)
    if db_dish is None:
        raise HTTPException(status_code=400, detail="Блюдо с таким названием уже есть")
    new_dish: models.Dish = await create_dish(async_session, dish)
    return new_dish

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
