from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app, get_db

from ..models import Dish, Ingredient

SQLALCHEMY_DATABASE_URL = 'sqlite://'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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


@app.on_event("startup")
def startup_event(session: Session = Depends(get_db)):
    print(session)
    ingredients = session.scalars(
        insert(Ingredient).returning(Ingredient),
        [
            {'title': 'ingredient1'},
            {'title': 'ingredient2'},
            {'title': 'ingredient3'}
        ]
    )

    session.execute(
        insert(Dish),
        [
            {'title': 'dish1', 'cooking_time': 1, 'description': 'description dish1', 'ingredients': ingredients},
        ]
    )


@app.on_event("shutdown")
def shutdown():
    engine.dispose()


def test_create_dish():
    response = client.post(
        '/dishes/',
        json={
            'title': 'dish1',
            'cooking_time': 60,
            'description': 'description1',
            'ingredients': [
                {
                    'title': 'ingredients1',
                },
                {
                    'title': 'ingredients2'
                }
            ]
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data['title'] == 'dish1'
    assert "id" in data
    dish_id = data['id']

    response = client.get(f'/dish/{dish_id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data.get('id') == dish_id
    assert data.get('title') == 'dish1'
    assert data.get('cooking_time') == 60
    assert data.get('description') == 'description1'
    assert data['ingredients'] == [{'title': 'ingredient1'}, {'title': 'ingredient2'}]
