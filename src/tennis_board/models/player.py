from typing import Dict, List
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tennis_board.db.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(default=None, primary_key=True, autoincrement=True)
    name: Mapped[str]

    matches: Mapped[List["Match"]] = relationship(
        primaryjoin="or_(Player.id == Match.player_one_id, Player.id == Match.player_two_id)",
        lazy="selectin",
    )

    matches_winner: Mapped[List["Match"]] = relationship(
        primaryjoin="and_(Player.id == Match.winner_id)",
        back_populates="winner",
        lazy="selectin",
    )

    __table_args__ = (Index("player_name_ind", "name", unique=True),)

    def to_dict_insert(self) -> Dict:
        return {
            "name": self.name,
        }
