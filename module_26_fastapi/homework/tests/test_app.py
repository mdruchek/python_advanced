import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from contextlib import asynccontextmanager
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db, engine
from .. import models
from sqlalchemy.pool import NullPool


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


def test_create_dish():
    dish_dict = {
        'title': 'dish2',
        'cooking_time': 60,
        'description': 'description2',
        'ingredients': [
            {
                'title': 'ingredients11',
            }
        ]
    }

    response = client.post('/dishes/', json=dish_dict)
    print(response.json())


def test_get_receipt():
    response = client.get('/dishes/')
    print(response.json())
    assert response.status_code == 200

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


# async def test_read_dishes():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    # response = client.get('/dishes/')
    # assert response.status_code == 200
    # data = response.json()
    # print(data)
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
#     pass
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

