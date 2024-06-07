import pytest


@pytest.mark.parametrize('route', ['/clients/1', '/clients'])
def test_route_status(app, web_client, route):
    rv = web_client.get(route)
    assert rv.status_code == 200


def test_create_client(web_client) -> None:
    user_data = {'name': 'Матвей', 'surname': 'Маскин',
                 'credit_card': 'creditka', 'car_number': 'х999хх999'}
    resp = web_client.post("/clients", json=user_data)

    assert resp.status_code == 201


def test_get_user(web_client):
    resp = web_client.get('/clients')
    assert resp.status_code == 200


def test_app_config(app):
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite://"
