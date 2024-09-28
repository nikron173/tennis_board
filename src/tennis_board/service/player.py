from typing import List
from tennis_board.dto.player import PlayerCreate, PlayerDto, PlayerMatchesDto
from tennis_board.repositories.player import PlayerRepository
from tennis_board.mapper.player import (
    players_to_dto,
    player_to_dto,
    player_with_matches_to_dto,
    player_create_to_player,
)


class PlayerService:
    def __init__(self, player_repo: PlayerRepository) -> None:
        self.player_repo = player_repo

    def find_all(self) -> List[PlayerDto]:
        players = self.player_repo.find_all()
        return players_to_dto(players)

    def find_by_name(self, player_name: str) -> PlayerDto | None:
        player = self.player_repo.find_by_name(player_name)
        if not player:
            return None
        return player_to_dto(player)

    def find_by_id(self, player_id: int) -> PlayerMatchesDto | None:
        player = self.player_repo.find_by_id(player_id)
        if not player:
            return None
        return player_with_matches_to_dto(player)

    def find_by_name_with_matches(self, player_name: str) -> PlayerMatchesDto | None:
        player = self.find_by_name(player_name)
        if not player:
            return None
        return player_with_matches_to_dto(player)

    def save(self, player_create: PlayerCreate) -> PlayerDto:
        player = player_create_to_player(player_create)
        return player_to_dto(self.player_repo.save(player))
