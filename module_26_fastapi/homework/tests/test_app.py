import datetime
from time import sleep

from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declarative_base

from ..database import Base
from ..main import app, get_db


SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# @app.on_event('startup')
# def startup_event(session: Session = Depends(get_db)):
#     Base.metadata.create_all(engine)
#
#     ingredients = session.scalars(
#         insert(Ingredient).returning(Ingredient),
#         [
#             {'title': 'ingredient1'},
#             {'title': 'ingredient2'},
#             {'title': 'ingredient3'}
#         ]
#     )
#
#     session.execute(
#         insert(Dish),
#         [
#             {'title': 'dish1', 'cooking_time': 1, 'description': 'description dish1', 'ingredients': ingredients},
#         ]
#     )
#
#
# @app.on_event("shutdown")
# def shutdown():
#     Base.metadata.drop_all(engine)
#     engine.dispose()
#
#
def test_create_dish():
    dish_dict = {
        'title': 'dish2',
        'cooking_time': 60,
        'description': 'description2',
        'ingredients': [
            {
                'title': 'ingredients11',
            },
            {
                'title': 'ingredients21'
            }
        ]
    }

    response = client.post('/dishes/', json=dish_dict)

    # assert response.status_code == 200
    # data: dict = response.json()
    # assert data.get('title') == dish_dict['title']
    # assert "id" in data
    #
    # assert data.get('id') == 1
    # assert data.get('title') == dish_dict['title']
    # assert data.get('cooking_time') == dish_dict['cooking_time']
    # assert data.get('description') == dish_dict['description']
    # assert data.get('ingredients') == [{'title': dish_dict['ingredients'][0]}, {'title': dish_dict['ingredients'][1]}]


# def test_read_dishes():
#     response = client.get(f'/dishes/')
#     assert response.status_code == 200
#     data = response.json()
#     assert data == [
#         {
#             'id': 1,
#             'title': 'dish1',
#             'cooking_time': 1,
#             'description': 'description dish1',
#             'ingredients': [
#                 {'title': 'ingredient1'},
#                 {'title': 'ingredient2'},
#                 {'title': 'ingredient3'}
#             ]
#         },
#         {
#             'id': 2,
#             'title': 'dish2',
#             'cooking_time': 60,
#             'description': 'description2',
#             'ingredients': [
#                 {
#                     'title': 'ingredients11',
#                 },
#                 {
#                     'title': 'ingredients21'
#                 }
#             ]
#         }
#     ]
#
#
# def test_read_dish():
#     response = client.get('/dishes/1')
#     assert response.status_code == 200
#     data = response.json()
#     assert data == {
#         'id': 1,
#         'title': 'dish1',
#         'cooking_time': 1,
#         'description': 'description dish1',
#         'ingredients': [
#             {'title': 'ingredient1'},
#             {'title': 'ingredient2'},
#             {'title': 'ingredient3'}
#         ]
#     }
#
#     response = client.get(f'/dishes/3')
#     assert response.status_code == 400
#     data = response.json()
#     assert data == {
#         'message': 'Блюдо не найдено'
#     }
#
#
# def test_update_dish():
#     response = client.patch(
#         '/dishes/1',
#         json={
#             'title': 'dish3',
#             'cooking_time': 63,
#             'description': 'description3',
#             'ingredients': [
#                 {
#                     'title': 'ingredients13',
#                 },
#                 {
#                     'title': 'ingredients23'
#                 }
#             ]
#         }
#     )
#
#     data = response.json()
#     assert data == {
#         'title': 'dish3',
#         'cooking_time': 63,
#         'description': 'description3',
#         'ingredients': [
#             {
#                 'title': 'ingredients13',
#             },
#             {
#                 'title': 'ingredients23'
#             }
#         ]
#     }
#
#     response = client.patch('/dishes/3')
#     assert response.status_code == 400
#     data = response.json()
#     assert data == {
#         'message': 'Блюдо не найдено'
#     }
#
#
# def test_delete_dish():
#     response = client.delete('/dishes/1')
#     assert response.json() == {'message': f'Блюдо 1 успешно удалено'}
#
#     response = client.delete('/dishes/1')
#     assert response.status_code == 400
#     data = response.json()
#     assert data == {
#         'message': 'Блюдо не найдено'
#     }
