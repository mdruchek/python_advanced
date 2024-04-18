import asyncio
from typing import AsyncGenerator
import sys
from copy import deepcopy

import pytest
import pytest_asyncio

from contextlib import asynccontextmanager
from httpx import AsyncClient, ASGITransport, WSGITransport
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import NullPool, StaticPool
from sqlalchemy import MetaData
import httpx

sys.path.append('../homework')


from ..main import app
from ..crud import del_dish


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


dish_dict_for_tests = {
    'title': 'test_dish',
    'cooking_time': 0,
    'description': 'test_dish_description',
    'ingredients': [
        {
            'title': 'test_ingredients'
        }
    ]
}

dish_id_test: int


async def test_create_dish(ac):
    dish_dict_for_create_dish = deepcopy(dish_dict_for_tests)
    response = await ac.post('/dishes/', json=dish_dict_for_create_dish)
    response_data = response.json()
    global dish_id_test
    dish_id_test = response_data.pop('id')
    response_data['ingredients'][0].pop('id')
    dish_dict_for_create_dish['number_views'] = 0
    assert response.status_code == 200
    assert response_data == dish_dict_for_create_dish


async def test_read_dishes(ac):
    dish_dict_for_read_dishes = deepcopy(dish_dict_for_tests)
    response = await ac.get('/dishes/')
    response_data = response.json()
    assert response.status_code == 200
    test_response_data = response_data.pop()
    test_response_data.pop('id')
    dish_dict_for_read_dishes.pop('ingredients')
    dish_dict_for_read_dishes.pop('description')
    dish_dict_for_read_dishes['number_views'] = 0
    assert test_response_data == dish_dict_for_read_dishes


async def test_read_dish(ac):
    dish_dict_for_read_dish = deepcopy(dish_dict_for_tests)
    response = await ac.get(f'/dishes/{dish_id_test}')
    assert response.status_code == 200
    response_data = response.json()
    response_data.pop('id')
    response_data['ingredients'][0].pop('id')
    assert response_data == dish_dict_for_read_dish


async def test_update_dish(ac):
    dict_dish_for_update = {
        'title': 'test_dish_2',
        'cooking_time': 1,
        'description': 'test_dish_description',
        'ingredients': [
            {
                'title': 'test_ingredients',
            },
            {
                'title': 'test_ingredients2'
            }
        ]
    }
    response = await ac.patch(
        f'/dishes/{dish_id_test}',
        json=dict_dish_for_update
    )

    response_data = response.json()

    response_data.pop('id')
    response_data['ingredients'][0].pop('id')
    response_data['ingredients'][1].pop('id')
    dict_dish_for_update['number_views'] = 1
    assert response_data == dict_dish_for_update


async def test_delete_dish(ac):
    response = await ac.delete(f'/dishes/{dish_id_test}')
    assert response.status_code == 200
    assert 'успешно удалено' in response.json().get('message')
