from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from tennis_board.db.database import Base
from tennis_board.models.player import Player


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, default=None, autoincrement=True)

    uuid: Mapped[UUID]

    player_one_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE", name="fk_player_one_id"),
    )

    player_two_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE", name="fk_player_two_id"),
    )

    winner_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE", name="fk_winner_id"),
    )

    winner: Mapped["Player"] = relationship(
        foreign_keys=winner_id,
        back_populates="matches_winner",
        lazy="joined",
    )

    player_one: Mapped["Player"] = relationship(
        foreign_keys=player_one_id,
        back_populates="matches",
        lazy="joined",
    )

    player_two: Mapped["Player"] = relationship(
        foreign_keys=player_two_id,
        back_populates="matches",
        lazy="joined",
    )

    score: Mapped[str] = mapped_column(nullable=True)

    def to_dict_insert(self):
        return {
            "uuid": self.uuid,
            "player_one_id": self.player_one_id,
            "player_two_id": self.player_two_id,
            "winner_id": self.winner_id,
            "score": self.score,
        }
