from http import client
from typing import Tuple, List
from tennis_board.exception.errors import ApplicationError
from tennis_board.service.player import PlayerService
from tennis_board.config import templates
from tennis_board.mapper.player import to_player_created
from tennis_board.utils.helpers import generate_headers


def get_players(service: PlayerService) -> Tuple[bytes, str, List[Tuple]]:
    players = service.find_all()
    template = templates.get_template("players.html")
    body = template.render(players=players, title="players").encode()
    header = generate_headers(body)
    return body, f"{client.OK} OK", header


def get_player_by_name(
    service: PlayerService, player_name: str
) -> Tuple[bytes, str, List[Tuple]]:
    player = service.find_by_name(player_name)
    if not player:
        template = templates.get_template("error.html")
        body = template.render(message="Page not found", title="error").encode()
        header = generate_headers(body)
        return (body, f"{client.NOT_FOUND} NOT_FOUND", header)
    template = templates.get_template("player.html")
    body = template.render(player=player, title="player").encode()
    header = generate_headers(body)
    return body, f"{client.OK} OK", header


def get_player_by_id(
    service: PlayerService, player_id: int
) -> Tuple[bytes, str, List[Tuple]]:
    player = service.find_by_id(player_id)
    if not player:
        template = templates.get_template("error.html")
        body = template.render(message="Page not found", title="error").encode()
        header = generate_headers(body)
        return (body, f"{client.NOT_FOUND} NOT_FOUND", header)
    template = templates.get_template("player.html")
    body = template.render(player=player, title="player").encode()
    header = generate_headers(body)
    return body, f"{client.OK} OK", header


def get_player_with_matches(
    service: PlayerService, player_name: str
) -> Tuple[bytes, str, List[Tuple]]:
    player = service.find_by_name_with_matches(player_name)
    if not player:
        template = templates.get_template("error.html")
        body = template.render(message="Page not found", title="error").encode()
        header = generate_headers(body)
        return (body, f"{client.NOT_FOUND} NOT_FOUND", header)
    template = templates.get_template("player_with_matches.html")
    body = template.render(player=player, title="player").encode()
    header = generate_headers(body)
    return body, f"{client.OK} OK", header


def create_player(service: PlayerService, data: str) -> Tuple[bytes, str, List[Tuple]]:
    try:
        player = to_player_created(data)
        player = service.save(player)
    except ApplicationError as e:
        template = templates.get_template("error.html")
        template = templates.get_template("error.html")
        body = template.render(message=e.message, title="error").encode()
        header = generate_headers(body)
        return (body, f"{e.status_code} {e.status}", header)
    header = generate_headers(b"Redirecting...", {"Location": "/players"})
    return (b"Redirecting...", f"{client.FOUND} FOUND", header)
