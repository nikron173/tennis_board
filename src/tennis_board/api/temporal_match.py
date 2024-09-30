from typing import Tuple, List
import logging
from http import client
from uuid import UUID
from tennis_board.config import templates
from tennis_board.db.in_memory_db import InMemoryDB
from tennis_board.dto.match import MatchCreate
from tennis_board.dto.player import PlayerCreate
from tennis_board.dto.temporal_match import TemporalMatch
from tennis_board.exception.errors import ApplicationError
from tennis_board.service.match import MatchService
from tennis_board.service.player import PlayerService
from tennis_board.mapper.match import to_temporal_match_created
from tennis_board.utils.helpers import parse_request_form, generate_headers

logger = logging.getLogger(__name__)


def get_temporal_matches(db: InMemoryDB) -> Tuple[bytes, str, List[Tuple]]:
    temporal_matches = list(db.values())
    body = (
        templates.get_template("unfinished_matches.html")
        .render(title="Unfinished matches", matches=temporal_matches)
        .encode()
    )
    header = generate_headers(body)
    return body, f"{client.OK} OK", header


def post_temporal_match(
    db: InMemoryDB, match_service: MatchService, match_uuid: UUID, data: str
) -> Tuple[bytes, str, List[Tuple]]:
    logger.info("Поиск не сохраненнего матча: %s", match_uuid)
    temporal_match = db.get(match_uuid)
    if not temporal_match:
        template = templates.get_template("error.html")
        body = template.render(message="Page not found", title="error").encode()
        header = generate_headers(body)
        return (body, f"{client.NOT_FOUND} NOT_FOUND", header)
    logger.info("Найден не сохраненный матч: %s", temporal_match.uuid)
    logger.info("Сырые данные: %s", data)
    data_with_form = parse_request_form(data)
    logger.info("Спарсенные данные с сырых данных: %s", data_with_form)
    if data_with_form.get("player_one"):
        return _game(
            db,
            match_service,
            temporal_match,
            temporal_match.player_one,
            temporal_match.player_two,
        )
    if data_with_form.get("player_two"):
        return _game(
            db,
            match_service,
            temporal_match,
            temporal_match.player_two,
            temporal_match.player_one,
        )
    template = templates.get_template("match_score.html")
    body = template.render(temporal_match=temporal_match, title="match-score").encode()
    header = generate_headers(body)
    return (body, f"{client.OK} OK", header)


def _game(
    db: InMemoryDB,
    match_service: MatchService,
    match: TemporalMatch,
    player,
    comparative_player,
) -> Tuple[bytes, str, List[Tuple]]:
    player.add_point()
    if (
        player.tie_break
        and comparative_player.tie_break
        and player.check_win_tie_break(comparative_player)
    ):
        return _win_player(db, match_service, match, player, comparative_player)
    elif player.check_win_game(comparative_player):
        player.add_game()
        player.point = 0
        comparative_player.point = 0
    if player.check_win(comparative_player):
        return _win_player(db, match_service, match, player, comparative_player)
    template = templates.get_template("match_score.html")
    body = template.render(temporal_match=match, title="match-score").encode()
    header = generate_headers(body)
    return (body, f"{client.OK} OK", header)


def _win_player(
    db: InMemoryDB,
    match_service: MatchService,
    match: TemporalMatch,
    player,
    comparative_player,
) -> Tuple[bytes, str, List[Tuple]]:
    match.set_player_winner_id(match.player_one_id)
    match_create = MatchCreate(
        match.uuid,
        match.player_one_id,
        match.player_two_id,
        match.player_winner_id,
        f"{player.game} : {comparative_player.game}",
    )
    match_service.save(match_create)
    del db[match.uuid]
    logger.info("Удален матч с uuid '%s' c in_memory_db", match.uuid)
    header = generate_headers(b"Redirecting...", {"Location": "/matches"})
    return b"Redirecting...", f"{client.FOUND} FOUND", header


def get_temporal_match(
    db: InMemoryDB, match_uuid: UUID
) -> Tuple[bytes, str, List[Tuple]]:
    temporal_match = db.get(match_uuid)
    if not temporal_match:
        template = templates.get_template("error.html")
        body = template.render(message="Page not found", title="error").encode()
        header = generate_headers(body)
        return (body, f"{client.NOT_FOUND} NOT_FOUND", header)
    template = templates.get_template("match_score.html")
    body = template.render(temporal_match=temporal_match, title="match-score").encode()
    header = generate_headers(body)
    return (body, f"{client.OK} OK", header)


def create_temporal_match(
    db: InMemoryDB, player_service: PlayerService, data: str
) -> Tuple[bytes, str, List[Tuple]]:
    try:
        logger.info("Создание TemporalMatch")
        new_temporal_match = to_temporal_match_created(data)
        logger.info(
            "Создался TemporalMatch.uuid: %s, player_one_name: %s, player_two_name: %s",
            new_temporal_match.uuid,
            new_temporal_match.player_one.name,
            new_temporal_match.player_two.name,
        )
        player_one = player_service.find_by_name(new_temporal_match.player_one.name)
        if not player_one:
            player_one = player_service.save(
                PlayerCreate(new_temporal_match.player_one.name)
            )
        new_temporal_match.set_player_one_id(player_one.player_id)
        player_two = player_service.find_by_name(new_temporal_match.player_two.name)
        if not player_two:
            player_two = player_service.save(
                PlayerCreate(new_temporal_match.player_two.name)
            )
        new_temporal_match.set_player_two_id(player_two.player_id)
        db[new_temporal_match.uuid] = new_temporal_match
    except ApplicationError as e:
        template = templates.get_template("error.html")
        body = template.render(message=e.message, title="error").encode()
        header = generate_headers(body)
        return (body, f"{e.status_code} {e.status}", header)
    header = generate_headers(
        b"Redirecting...", {"Location": f"/match-score?uuid={new_temporal_match.uuid}"}
    )
    return (
        b"Redirecting...",
        f"{client.FOUND} FOUND",
        header,
    )
