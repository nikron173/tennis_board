import re
import uuid
from typing import Any
from http import client
from tennis_board.config import templates
from tennis_board.db.in_memory_db import InMemoryDB
from tennis_board.service.match import MatchService
from tennis_board.service.player import PlayerService
from tennis_board.api.player import (
    get_players,
    create_player,
    get_player_by_id,
)
from tennis_board.api.temporal_match import (
    create_temporal_match,
    get_temporal_match,
    post_temporal_match,
    get_temporal_matches,
)
from tennis_board.api.match import (
    get_matches,
)
from tennis_board.utils.helpers import generate_headers, not_found, parse_request_form


class Application:
    def __init__(
        self,
        player_service: PlayerService,
        match_service: MatchService,
        in_memory_db: InMemoryDB,
    ) -> None:
        self.player_service = player_service
        self.match_service = match_service
        self.memory_db = in_memory_db

    def __call__(self, environ, start_response) -> Any:
        header = None
        match (environ["REQUEST_URI"], environ["REQUEST_METHOD"]):
            case ("/", "GET"):
                status = f"{client.OK} OK"
                body = templates.get_template("base.html").render(title="Home").encode()
            case ("/new-match", "POST"):
                data = environ["wsgi.input"].read().decode()
                body, status, header = create_temporal_match(
                    self.memory_db, self.player_service, data
                )
            case ("/new-match", "GET"):
                status = f"{client.OK} OK"
                body = (
                    templates.get_template("new_match.html")
                    .render(title="New match")
                    .encode()
                )

            case path_method if re.findall(
                r"^/match-score\?uuid=[-a-z0-9]+$", path_method[0]
            ) and path_method[1] == "GET":
                match_uuid = uuid.UUID(path_method[0].replace("/match-score?uuid=", ""))
                body, status, header = get_temporal_match(self.memory_db, match_uuid)
            case path_method if re.findall(
                r"^/match-score\?uuid=[a-z0-9-]+$", path_method[0]
            ) and path_method[1] == "POST":
                match_uuid = uuid.UUID(
                    str(path_method[0]).replace("/match-score?uuid=", "")
                )
                data = environ["wsgi.input"].read().decode()
                match_uuid = uuid.UUID(
                    str(path_method[0]).replace("/match-score?uuid=", "")
                )
                body, status, header = post_temporal_match(
                    self.memory_db, self.match_service, match_uuid, data
                )
            case path_method if re.findall(
                r"^/matches(\?(page=\d+)?(&filter_by_player_name=\w+)?(filter_by_player_name=\w+)?(&page=\d+)?)?$",
                path_method[0],
            ) and path_method[1] == "GET":
                query = environ["QUERY_STRING"]
                if not query:
                    body, status, header = get_matches(self.match_service)
                else:
                    data = parse_request_form(query)
                    page = 0
                    if data.get("page") and int(data.get("page")) > 0:
                        page = int(data.get("page"))

                    filter_player = None
                    if data.get("filter_by_player_name"):
                        filter_player = data.get("filter_by_player_name")

                    body, status, header = get_matches(
                        self.match_service, page, filter_player
                    )

            case path_method if re.findall(
                r"^/player/[0-9]+$", path_method[0]
            ) and path_method[1] == "GET":
                player_id = int(path_method[0].replace("/player/", ""))
                body, status, header = get_player_by_id(self.player_service, player_id)

            case ("/players", "GET"):
                body, status, header = get_players(self.player_service)

            case ("/players", "POST"):
                data = environ["wsgi.input"].read().decode()
                body, status, header = create_player(self.player_service, data)
            case ("/unfinished_matches", "GET"):
                body, status, header = get_temporal_matches(self.memory_db)
            case _:
                body = not_found(environ["PATH_INFO"])
                status = f"{client.NOT_FOUND} NOT_FOUND"

        if not header:
            header = generate_headers(body)

        start_response(
            status,
            header,
        )
        return [body]
