import logging
from typing import List
from sqlalchemy import delete, select, insert
from sqlalchemy.orm import sessionmaker

from tennis_board.models.player import Player

logger = logging.getLogger(__name__)


class PlayerRepository:
    def __init__(self, pool_session: sessionmaker) -> None:
        self.pool_session = pool_session

    def find_by_id(self, player_id: int) -> Player | None:
        with self.pool_session() as session:
            stmt = select(Player).filter(Player.id == player_id)
            res = session.execute(stmt).scalar_one_or_none()
        return res

    def find_all(self) -> List[Player]:
        with self.pool_session() as session:
            stmt = select(Player)
            res = session.execute(stmt).scalars().all()
        logger.info("Find all players: %s", res)
        return res

    def find_by_name(self, player_name: str) -> Player | None:
        with self.pool_session() as session:
            stmt = select(Player).filter(Player.name == player_name)
            res = session.execute(stmt).scalar_one_or_none()
        return res

    def delete_by_id(self, player_id: int) -> None:
        with self.pool_session() as session:
            session.execute(delete(Player).filter(Player.id == player_id))
            session.commit()

    def delete_by_name(self, player_name: str) -> None:
        with self.pool_session() as session:
            session.execute(delete(Player).filter(Player.name == player_name))
            session.commit()

    def save(self, player: Player) -> Player:
        with self.pool_session() as session:
            stmt = insert(Player).values(player.to_dict_insert()).returning(Player.id)
            player_id = session.execute(stmt).scalar_one()
            session.commit()
            player.id = player_id
        return player
