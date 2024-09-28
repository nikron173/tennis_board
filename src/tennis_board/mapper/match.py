from typing import List
from http import client
import logging
from tennis_board.dto.match import MatchCreate, MatchDto
from tennis_board.dto.temporal_match import TemporalMatch
from tennis_board.models.match import Match
from tennis_board.utils.helpers import parse_request_form
from tennis_board.exception.errors import ApplicationError
from tennis_board.mapper.player import player_to_dto


logger = logging.getLogger(__name__)


def match_to_dto(match: Match) -> MatchDto:
    logger.info("Преобразование матча '%s' в MatchDto модель", match)
    return MatchDto(
        match_uuid=match.uuid,
        player_one=player_to_dto(match.player_one),
        player_two=player_to_dto(match.player_two),
        winner=player_to_dto(match.winner),
        score=match.score,
    )


def matches_to_dto(matches: List[Match]) -> List[MatchDto]:
    return list(map(match_to_dto, matches))


# def to_match_created(data: str) -> MatchCreate:
#     data_with_form = parse_request_form(data)
#     player_one_name = data_with_form.get("player_one_name")
#     player_two_name = data_with_form.get("player_two_name")
#     if player_one_name and player_two_name:
#         raise ApplicationError(
#             client.BAD_REQUEST, "BAD_REQUEST", "Players names not valid or is none"
#         )
#     return MatchCreate(player_one_name=player_one_name, player_two_name=player_two_name)


def to_temporal_match_created(data: str) -> TemporalMatch:
    data_with_form = parse_request_form(data)
    player_one_name = data_with_form.get("player_one_name")
    player_two_name = data_with_form.get("player_two_name")
    logger.info(
        "Player_one_name: %s, Player_two_name: %s",
        player_one_name,
        player_two_name,
    )
    if not (player_one_name and player_two_name):
        raise ApplicationError(
            client.BAD_REQUEST, "BAD_REQUEST", "Players names not valid or is none"
        )
    logger.info(
        "Преобразование из сырых данных в TemporalMatch: player_one_name: %s, player_two_name: %s",
        player_one_name,
        player_two_name,
    )
    return TemporalMatch(
        player_one_name=player_one_name, player_two_name=player_two_name
    )
