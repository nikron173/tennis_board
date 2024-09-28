from http import client
from typing import Tuple
from tennis_board.exception.errors import ApplicationError
from tennis_board.service.player import PlayerService
from tennis_board.config import templates
from tennis_board.mapper.player import to_player_created
from tennis_board.utils.helpers import generate_headers


def get_players(service: PlayerService) -> Tuple:
    players = service.find_all()
    template = templates.get_template("players.html")
    return template.render(players=players, title="players").encode(), f"{client.OK} OK"


def get_player_by_name(service: PlayerService, player_name: str) -> Tuple[
    bytes,
    str,
]:
    player = service.find_by_name(player_name)
    if not player:
        template = templates.get_template("error.html")
        return (
            template.render(message="Page not found", title="error").encode(),
            f"{client.NOT_FOUND} NOT_FOUND",
        )
    template = templates.get_template("player.html")
    return template.render(player=player, title="player").encode(), f"{client.OK} OK"


def get_player_by_id(service: PlayerService, player_id: int) -> Tuple:
    player = service.find_by_id(player_id)
    if not player:
        template = templates.get_template("error.html")
        return (
            template.render(message="Page not found", title="error").encode(),
            f"{client.NOT_FOUND} NOT_FOUND",
        )
    template = templates.get_template("player.html")
    return template.render(player=player, title="player").encode(), f"{client.OK} OK"


def get_player_with_matches(service: PlayerService, player_name: str) -> Tuple:
    player = service.find_by_name_with_matches(player_name)
    if not player:
        template = templates.get_template("error.html")
        return (
            template.render(message="Page not found", title="error").encode(),
            f"{client.NOT_FOUND} NOT_FOUND",
        )
    template = templates.get_template("player_with_matches.html")
    return template.render(player=player, title="player").encode(), f"{client.OK} OK"


def create_player(service: PlayerService, data: str) -> Tuple:
    try:
        player = to_player_created(data)
        player = service.save(player)
    except ApplicationError as e:
        template = templates.get_template("error.html")
        return (
            template.render(message=e.message, title="error").encode(),
            f"{e.status_code} {e.status}",
        )
    return (b"Redirecting...", f"{client.FOUND} FOUND")
