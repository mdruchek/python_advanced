from flask import Blueprint, jsonify

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func, text

from .db import get_db, close_db
from .models import User, Coffee


bp = Blueprint('user', __name__)


@bp.route('/create', methods=['POST'])
def create_user():
    db = get_db()

    insert_query = (
        insert(User)
        .returning(
            User.id,
            User.name,
            User.address,
            User.coffee_id
        )
        .values(
            name='Лев',
            has_sale=True,
            address={
                'country': 'Russia',
                'city': 'Moscow',
                'street_name': 'Волжский бульвар',
                'building_number': '11'
            },
            coffee_id='1'
        )
    )

    result = db.execute(insert_query).fetchone()
    coffee_id = result[3]
    coffee_name = db.execute(select(Coffee.title).where(Coffee.id == coffee_id)).scalar()

    db.commit()
    close_db()
    if result:
        result_json = dict(
            id=result[0],
            name=result[1],
            address=result[2],
            coffee=coffee_name
        )

        return jsonify(result_json)


@bp.route('/search_coffee_on_title/<string:title>', methods=['GET'])
def search_coffee_on_title(title):
    db = get_db()
    query = select(Coffee).where(Coffee.title.match(title))
    coffee = db.execute(query).scalars().all()
    coffee_list = [obj.to_json() for obj in coffee]
    return jsonify(coffee_list)


@bp.route('/unique_elements_in_coffee_notes', methods=['GET'])
def unique_elements_in_coffee_notes():
    db = get_db()

    query = (select(func.string_to_table(func.string_agg(func.array_to_string(Coffee.notes, ' '), ' '), ' ')
                    .label('notes'))
             .distinct()
             .order_by('notes'))

    response = db.execute(query)
    notes = response.scalars().all()
    return jsonify({'unique_notes': notes})


@bp.route('/users_residing_in_country/<string:country>', methods=['GET'])
def users_residing_in_country(country):
    db = get_db()

    query = (select(User.name)
             .where(func.jsonb_path_match(func.to_jsonb(User.address), f'exists($.country ? (@ == "{country}"))')))

    users = db.execute(query).scalars().all()
    return jsonify({'users': users})
