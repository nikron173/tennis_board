import logging
from typing import List
from uuid import UUID
from sqlalchemy import select, delete, insert
from sqlalchemy.orm import sessionmaker

from tennis_board.models.match import Match


logger = logging.getLogger(__name__)


class MatchRepository:
    def __init__(self, pool_session: sessionmaker) -> None:
        self.pool_session = pool_session

    def find_by_id(self, match_id: int) -> Match:
        with self.pool_session() as session:
            stmt = select(Match).filter(Match.id == match_id)
            res = session.execute(stmt).scalar_one_or_none()
        return res

    def find_all(self) -> List[Match]:
        logger.info("Поиск всех матчей")
        with self.pool_session() as session:
            stmt = select(Match)
            res = session.execute(stmt).scalars().all()
        logger.info("Найденные матчи: %s", res)
        return res

    def find_by_uuid(self, match_uuid: UUID) -> Match | None:
        with self.pool_session() as session:
            stmt = select(Match).filter(Match.uuid == match_uuid)
            res = session.execute(stmt).scalar_one_or_none()
        return res

    def delete_by_uuid(self, match_uuid: UUID) -> None:
        with self.pool_session() as session:
            session.execute(delete(Match).filter(Match.uuid == match_uuid))
            session.commit()

    def save(self, match: Match) -> Match:
        logger.info("Сохранение матча: %s", match.to_dict_insert())
        with self.pool_session() as session:
            stmt = insert(Match).values(match.to_dict_insert()).returning(Match.id)
            match_id = session.execute(stmt).scalar_one()
            match = session.get(Match, match_id)
            session.commit()
            session.refresh(match)
        logger.info("Матч с uuid: '%s' сохранен", match.uuid)
        logger.info("Сохраненный матч: %s", match)
        return match
