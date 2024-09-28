from typing import Tuple, List
import logging
from http import client
from uuid import UUID
from tennis_board.config import templates
from tennis_board.db.in_memory_db import InMemoryDB
from tennis_board.dto.match import MatchCreate
from tennis_board.dto.player import PlayerCreate
from tennis_board.exception.errors import ApplicationError
from tennis_board.service.match import MatchService
from tennis_board.service.player import PlayerService
from tennis_board.mapper.match import to_temporal_match_created
from tennis_board.utils.helpers import parse_request_form

logger = logging.getLogger(__name__)


def get_matches(match_service: MatchService) -> Tuple[bytes, str, List[Tuple]]:
    matches = match_service.find_all()
    template = templates.get_template("matches.html")
    return (
        template.render(matches=matches, title="matches").encode(),
        f"{client.OK} OK",
    )
