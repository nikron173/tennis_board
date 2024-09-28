import re
import uuid
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
            case ("/new-match", "POST"):
                data = environ["wsgi.input"].read().decode()
                result = create_temporal_match(
                    self.memory_db, self.player_service, data
                )
                if len(result) == 3:
                    body, status, match_uuid = result
                    header = generate_headers(
                        body, {"Location": f"/match-score?uuid={match_uuid}"}
                    )
                else:
                    body, status = result

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
                match_uuid = uuid.UUID(
                    str(path_method[0]).replace("/match-score?uuid=", "")
                )
                body, status = get_temporal_match(self.memory_db, match_uuid)

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
                result = post_temporal_match(
                    self.memory_db, self.match_service, match_uuid, data
                )
                if len(result) == 3:
                    body, status, add_header = result
                    header = self.generate_headers(body, add_header)
                else:
                    body, status = result

            case ("/matches", "GET"):
                body, status = get_matches(self.match_service)

            case path_method if re.findall(
                r"^/player/[0-9]+$", path_method[0]
            ) and path_method[1] == "GET":
                player_id = int(path_method[0].replace("/player/", ""))
                body, status = get_player_by_id(self.player_service, player_id)

            case ("/players", "GET"):
                body, status = get_players(self.player_service)

            case ("/players", "POST"):
                data = environ["wsgi.input"].read().decode()
                body, status = create_player(self.player_service, data)
                header = self.generate_headers(body, {"Location": "/players"})

            case ("/unfinished_matches", "GET"):
                body, status = get_temporal_matches(self.memory_db)
            case _:
                body = self.not_found(environ["PATH_INFO"])
                status = f"{client.NOT_FOUND} NOT_FOUND"

        start_response(
            status,
            header,
        )
        return [body]
