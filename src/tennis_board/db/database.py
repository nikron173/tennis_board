import logging
from uuid import uuid4

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from tennis_board.config import settings


logger = logging.getLogger(__name__)

engine = create_engine(
    url=settings.database_url,
    pool_size=settings.pool_size,
    echo=settings.is_sqlalchemy_echo,
)

session_factory = sessionmaker(engine, autoflush=True)


class Base(DeclarativeBase):

    repr_cols_num = 7
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


def create_tables():
    logger.info("Удаление таблиц")
    Base.metadata.drop_all(engine)
    logger.info("Выполнено удаление таблиц")
    Base.metadata.create_all(engine)
    logger.info("Выполнено создание таблиц")


def insert_data():
    logger.info("Вставка данных")
    with session_factory() as session:
        session.execute(
            text("INSERT INTO players (name) VALUES (:name)"),
            [
                {"name": "Nikita"},
                {"name": "Masha"},
                {"name": "Andrey"},
                {"name": "Kirill"},
                {"name": "Nika"},
            ],
        )

        session.execute(
            text(
                "INSERT INTO matches (uuid, player_one_id, player_two_id, winner_id) VALUES (:uuid, :p1, :p2, :w)"
            ),
            [
                {"uuid": uuid4(), "p1": 1, "p2": 2, "w": 1},
                {"uuid": uuid4(), "p1": 2, "p2": 3, "w": 3},
                {"uuid": uuid4(), "p1": 1, "p2": 3, "w": 1},
                {"uuid": uuid4(), "p1": 3, "p2": 4, "w": 4},
                {"uuid": uuid4(), "p1": 5, "p2": 2, "w": 5},
            ],
        )
        session.commit()
    logger.info("Вставка данных выполнена успешно")
