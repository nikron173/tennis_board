from typing import Tuple, List
import logging
from http import client
from tennis_board.config import templates
from tennis_board.service.match import MatchService
from tennis_board.utils.helpers import generate_headers

logger = logging.getLogger(__name__)


def get_matches(
    match_service: MatchService, page: int = 0, filter_player: str = ""
) -> Tuple[bytes, str, List[Tuple]]:
    if filter_player:
        matches = match_service.find_by_player_name(filter_player, page)
        pages = match_service.count_pages(filter_player)
    else:
        matches = match_service.find_all(page)
        pages = match_service.count_pages()

    if len(matches) == 0:
        template = templates.get_template("error.html")
        body = template.render(message="Page not found", title="error").encode()
        header = generate_headers(body)
        return (body, f"{client.NOT_FOUND} NOT_FOUND", header)

    template = templates.get_template("matches.html")
    body = template.render(
        matches=matches, title="matches", pages=pages, url_page="matches"
    ).encode()
    header = generate_headers(body)
    return (body, f"{client.OK} OK", header)
