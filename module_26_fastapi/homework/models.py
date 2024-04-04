from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey

from database import Base


dish_ingredient_table = Table(
    'dish_ingredient_table',
    Base.metadata,
    Column('Dish', ForeignKey('Dish.id'), primary_key=True),
    Column('Ingredient', ForeignKey('Ingredient.id'), primary_key=True)
)


class Dish(Base):
    __tablename__ = 'Dish'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    number_views: Mapped[int] = mapped_column(nullable=False, default=0)
    description: Mapped[str] = mapped_column(nullable=False)

    ingredients: Mapped[list['Ingredient']] = relationship(
        secondary=dish_ingredient_table, back_populates='dishes'
    )


class Ingredient(Base):
    __tablename__ = 'Ingredient'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    dishes: Mapped[list['Dish']] = relationship(
        secondary=dish_ingredient_table, back_populates='ingredients'
    )