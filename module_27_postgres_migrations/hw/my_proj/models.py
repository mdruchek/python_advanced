from typing import Optional, Any
from typing_extensions import Annotated

from sqlalchemy import String, Integer, Sequence, ARRAY, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


str50 = Annotated[str, 50]
str100 = Annotated[str, 100]
str200 = Annotated[str, 200]


class Base(DeclarativeBase):
    type_annotation_map = {
        str50: String(50),
        str100: String(100),
        str200: String(200)
    }


class Coffee(Base):
    __tablename__ = 'coffee'

    id: Mapped[int] = mapped_column(Integer, Sequence('coffee_id_seq'),  primary_key=True)
    title: Mapped[str200]
    origin: Mapped[Optional[str200]]
    intensifier: Mapped[Optional[str100]]
    notes: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))

    users: Mapped[list['User']] = relationship(back_populates='coffee')

    def to_json(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str50]
    surname: Mapped[Optional[str50]]
    patronomic: Mapped[Optional[str50]]
    has_sale: Mapped[Optional[bool]] = mapped_column(default=False)
    address: Mapped[Optional[dict[str, str]]] = mapped_column(JSON)
    coffee_id: Mapped[Coffee] = mapped_column(ForeignKey('coffee.id'))

    coffee: Mapped['Coffee'] = relationship(back_populates='users')

    def to_json(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
