from typing import List
from http import client
from tennis_board.dto.player import PlayerDto, PlayerMatchesDto, PlayerCreate
from tennis_board.exception.errors import ApplicationError
from tennis_board.models.player import Player
from tennis_board.utils.helpers import parse_request_form


def player_to_dto(player: Player) -> PlayerDto:
    return PlayerDto(player.id, player.name)


def players_to_dto(players: List[Player]) -> List[PlayerDto]:
    return list(map(player_to_dto, players))


def player_with_matches_to_dto(player: Player) -> PlayerMatchesDto:
    return PlayerMatchesDto(
        player.id, player.name, player.matches, player.matches_winner
    )


def to_player_created(data: str) -> PlayerCreate:
    data_with_form = parse_request_form(data)
    player_name = data_with_form.get("player_name")
    if not player_name:
        raise ApplicationError(
            client.BAD_REQUEST, "BAD_REQUEST", "Player name not valid or is none"
        )
    return PlayerCreate(player_name)


def player_create_to_player(player_create: PlayerCreate) -> Player:
    return Player(name=player_create.name)
