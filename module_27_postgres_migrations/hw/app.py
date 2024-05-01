# from typing_extensions import Annotated
# from typing import Optional, List, Dict
#
# from flask import Flask, g
#
# from sqlalchemy import event, create_engine, Sequence, String, Integer, ForeignKey, Column
# from sqlalchemy.engine import Engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship, declarative_base
# from sqlalchemy.dialects.postgresql import ARRAY, JSON
#
#
# app = Flask(__name__)
#
# engine = create_engine('postgresql+psycopg2://admin:admin@localhost')
# Session = sessionmaker(bind=engine)
# session = Session()
#
# str50 = Annotated[str, 50]
# str100 = Annotated[str, 100]
# str200 = Annotated[str, 200]
#
#
# class Base(DeclarativeBase):
#     type_annotation_map = {
#         str50: String(50),
#         str100: String(100),
#         str200: String(200)
#     }
#
#
# class Coffee(Base):
#     __tablename__ = 'coffee'
#
#     id: Mapped[int] = mapped_column(Integer, Sequence('coffee_id_seq'), primary_key=True)
#     title: Mapped[str200]
#     origin: Mapped[Optional[str200]]
#     intensifier: Mapped[Optional[str100]]
#     notes: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
#
#     users: Mapped[list['User']] = relationship(back_populates='user')
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(Integer, Sequence('user_id_seq'), primary_key=True)
#     name: Mapped[str50]
#     has_sale: Mapped[Optional[bool]]
#     address: Mapped[Optional[dict[str, str]]] = mapped_column(JSON)
#     coffee_id: Mapped[Coffee] = mapped_column(ForeignKey('coffee.id'))
#
#     coffee: Mapped['Coffee'] = relationship(back_populates='users')
#
#
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#
#
# @app.route('/', methods=['GET'])
# def main_route():
#     return 'привет'
#
#
# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)
