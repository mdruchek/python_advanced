from time import sleep
import click
import requests
import random

from flask import current_app, g, Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Coffee, User


engine = create_engine(current_app.config['DATABASE'], echo=True)
Session = sessionmaker(bind=engine)


def get_db():
    if 'db' not in g:
        session = Session()
        g.db = session
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@click.command('init_db')
@click.option('--fwd', is_flag=True, default=False, help='Fill with data')
def init_db_command(fwd):
    init_db()
    click.echo('Initialized the database.')
    if fwd:
        users_names = [
            'Иван',
            'Пётр',
            'Михаил',
            'Татьяна',
            'Ольга',
            'Владимир',
            'Александр',
            'Ксения',
            'Захар',
            'Олег'
        ]

        users_list = []
        coffee_list = []

        users_names = random.sample(users_names, k=len(users_names))
        coffee_id = random.sample(range(1, 11), k=10)

        while True:
            r = requests.get('https://random-data-api.com/api/coffee/random_coffee')

            if r.status_code == 200 and len(coffee_list) < 10:
                data = r.json()

                coffee_obj = Coffee(
                    title=data['blend_name'],
                    origin=data['origin'],
                    notes=data['notes'].split(', '),
                    intensifier=data['intensifier']
                )

                coffee_list.append(coffee_obj)
                click.echo(f'Количество coffee: {len(coffee_list)}')

            sleep(1)

            r = requests.get('https://random-data-api.com/api/address/random_address')

            if r.status_code == 200 and len(users_list) < 10:
                data = r.json()

                user_obj = User(
                    name=users_names.pop(),
                    has_sale=random.choice([True, False]),
                    address={
                        'country': data['country'],
                        'state': data['state'],
                        'city': data['city'],
                        'street_name': data['street_name'],
                        'building_number': data['building_number'],
                        'mail_box': data['mail_box']
                    },
                    coffee_id=coffee_id.pop()
                )

                users_list.append(user_obj)
                click.echo(f'Количество users: {len(users_list)}')

            if len(users_list) == 10 and len(coffee_list) == 10:
                break

            sleep(1)

        with Session() as session:
            session.add_all(coffee_list)
            session.add_all(users_list)
            session.commit()

        click.echo('The database is filled with initial data')


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
