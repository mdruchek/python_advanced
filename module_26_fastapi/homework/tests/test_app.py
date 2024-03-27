from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app, get_db

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
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


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
