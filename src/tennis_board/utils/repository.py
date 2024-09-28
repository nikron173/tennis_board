from abc import ABC, abstractmethod
from sqlalchemy import insert, select

from tennis_board.db.database import session_factory
from tennis_board.logger import logger


class AbstractRepository(ABC):

    @abstractmethod
    def find_one():
        raise NotImplementedError

    @abstractmethod
    def find_all():
        raise NotImplementedError

    @abstractmethod
    def save():  # -> Any:
        raise NotImplementedError

    @abstractmethod
    def update():
        raise NotImplementedError

    @abstractmethod
    def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: type = None

    def find_one(self, id: int):
        logger.info("Поиск %s по id: %d", self.model, id)
        with session_factory() as session:
            stmt = select(self.model).filter_by(id=id)
            res = session.execute(stmt).scalar_one_or_none()
        logger.info("Найдено %s по id: %s", res, id)
        return res

    def find_all(self):
        logger.info("Поиск всех %s", self.model)
        with session_factory() as session:
            stmt = select(self.model)
            res = session.execute(stmt).scalars().all()
        logger.info("Выполнен поиск всех %s, найдено: %d записей", self.model, len(res))
        return res

    def save(self, data: dict):
        logger.info("Сохранение записи %s с данными: %s", self.model, data)
        with session_factory() as session:
            stmt = insert(self.model).values(**data)
            res = session.execute(stmt).returns_rows
        logger.info("Выполнено сохранение %s, сохранено записей: %s", self.model, res)
        return res

    def update(self, data: dict):
        raise NotImplementedError

    def delete(self, data: dict):
        raise NotImplementedError
