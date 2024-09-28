from typing import List

from tennis_board.dto.match import MatchCreate, MatchDto
from tennis_board.models.match import Match
from tennis_board.repositories.match import MatchRepository
from tennis_board.repositories.player import PlayerRepository
from tennis_board.mapper.match import matches_to_dto, match_to_dto


class MatchService:
    def __init__(
        self, match_repo: MatchRepository, player_repo: PlayerRepository
    ) -> None:
        self.match_repo = match_repo
        self.player_repo = player_repo

    def find_all(self) -> List[MatchDto]:
        matches = self.match_repo.find_all()
        return matches_to_dto(matches)

    def save(self, match_create: MatchCreate) -> MatchDto:
        match = Match(
            uuid=match_create.uuid,
            player_one_id=match_create.player_one_id,
            player_two_id=match_create.player_two_id,
            winner_id=match_create.player_winner_id,
            score=match_create.score,
        )
        return match_to_dto(self.match_repo.save(match))
