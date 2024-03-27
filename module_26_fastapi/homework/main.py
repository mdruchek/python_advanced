from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession


from database import engine, async_session
from crud import models, schemas
import crud


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()


@app.post('/dishes', response_model=schemas.DishOut)
async def create_dish(dish: schemas.DishIn, session: AsyncSession = Depends(get_db)) -> models.Dish:
    # db_dish = await crud.get_dish_by_title(session=async_session, title=dish.title)
    # if db_dish is not None:
    #     raise HTTPException(status_code=400, detail='Блюдо с таким названием уже есть')
    new_dish: models.Dish = await crud.create_dish(session=session, dish=dish)
    return new_dish


@app.get('/dishes', response_model=list[schemas.DishOut])
async def read_dishes(session: AsyncSession = Depends(get_db)) -> list[models.Dish]:
    dishes = await crud.get_dishes(session)
    if not dishes:
        raise HTTPException(status_code=404, detail='В базеданных ничего нет')
    return dishes


@app.get('/dishes/{dish_id}', response_model=schemas.DishOut)
async def read_dish(dish_id: int, session: AsyncSession = Depends(get_db)) -> models.Dish:
    dish = await crud.get_dish_by_id(session, dish_id=dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail='Блюдо не найдено')
    return dish


@app.patch('/dishes/{dish_id}', response_model=schemas.DishOut)
async def patch_dish(dish: schemas.DishUpdate, dish_id: int, session: AsyncSession = Depends(get_db)) -> models.Dish:
    ...


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
