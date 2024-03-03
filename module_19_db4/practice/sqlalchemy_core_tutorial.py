from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import insert
from sqlalchemy import create_engine
from sqlalchemy import select, bindparam
from sqlalchemy import func, cast

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj.create_all(engine)

stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()

scalar_subq = (
    select(user_table.c.id)
    .where(user_table.c.name == bindparam("username"))
    .scalar_subquery()
)
with engine.connect() as conn:
    result = conn.execute(
        insert(address_table).values(user_id=scalar_subq),
        [
            {
                "username": "spongebob",
                "email_address": "spongebob@sqlalchemy.org",
            },
            {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
            {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
        ],
    )
    conn.commit()
