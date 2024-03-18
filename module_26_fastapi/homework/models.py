from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Dish(Base):
    __tablename__ = 'Dish'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    cooking_time: Mapped[int] = mapped_column(nullable=False)


class
