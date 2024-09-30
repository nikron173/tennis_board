import logging
from typing import List
from uuid import UUID
from sqlalchemy import or_, select, delete, insert, func
from sqlalchemy.orm import aliased, sessionmaker

from tennis_board.models.match import Match
from tennis_board.models.player import Player


logger = logging.getLogger(__name__)


class MatchRepository:
    def __init__(self, pool_session: sessionmaker) -> None:
        self.pool_session = pool_session

    def find_by_id(self, match_id: int) -> Match:
        with self.pool_session() as session:
            stmt = select(Match).filter(Match.id == match_id)
            res = session.execute(stmt).scalar_one_or_none()
        return res

    def find_all(self, page: int = 0) -> List[Match]:
        logger.info("Поиск всех матчей")
        offset = 0 if page in [0, 1] else (page - 1) * 10
        with self.pool_session() as session:
            stmt = select(Match).limit(10).offset(offset)
            res = session.execute(stmt).scalars().all()
        logger.info("Найденные матчи: %s", res)
        return res

    def find_by_player_name(self, player_name: str, page: int = 0) -> List[Match]:
        logger.info("Поиск всех матчей по фильтру player_name: %s", player_name)
        offset = 0 if page in [0, 1] else (page - 1) * 10
        with self.pool_session() as session:
            p1 = aliased(Player)
            p2 = aliased(Player)
            stmt = (
                select(Match)
                .join(p1, p1.id == Match.player_one_id)
                .join(p2, p2.id == Match.player_two_id)
                .filter(
                    or_(
                        p1.name.contains(player_name),
                        p2.name.contains(player_name),
                    )
                )
                .offset(offset)
                .limit(10)
            )
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

    def count_pages(self, player_name: str = None) -> int:
        with self.pool_session() as session:
            p1 = aliased(Player)
            p2 = aliased(Player)
            if player_name:
                stmt = (
                    select(func.count(Match.id))
                    .join(p1, p1.id == Match.player_one_id)
                    .join(p2, p2.id == Match.player_two_id)
                    .filter(
                        or_(
                            p1.name.contains(player_name),
                            p2.name.contains(player_name),
                        )
                    )
                )
            else:
                stmt = select(func.count(Match.id))
            count_object = session.execute(stmt).scalar_one()
        return (
            int(count_object / 10)
            if count_object % 10 == 0
            else int(count_object / 10) + 1
        )
