import os
import logging
from waitress.server import create_server
from whitenoise import WhiteNoise
from tennis_board.app import Application
from tennis_board.db.in_memory_db import InMemoryDB
from tennis_board.repositories.match import MatchRepository
from tennis_board.repositories.player import PlayerRepository
from tennis_board.db.database import create_tables, insert_data, session_factory
from tennis_board.service.match import MatchService
from tennis_board.service.player import PlayerService
from tennis_board.logger import setup_logger

logger = logging.getLogger(__name__)


def main() -> None:
    pass
    # create_tables()
    # insert_data()
    # player_repo = PlayerRepository(session_factory)
    # match_repo = MatchRepository(session_factory)
    # print(match_repo.find_by_id(2).player_one)
    # print(player_repo.find_by_id(3).matches)
    # print(player_repo.find_by_id(3).matches_winner)


if __name__ == "__main__":
    setup_logger()
    create_tables()
    insert_data()
    memory_db = InMemoryDB()
    player_repo = PlayerRepository(session_factory)
    match_repo = MatchRepository(session_factory)
    player_service = PlayerService(player_repo)
    match_service = MatchService(match_repo, player_repo)
    app = Application(player_service, match_service, memory_db)

    app = WhiteNoise(
        app,
        root=os.path.join(
            os.path.dirname(__file__), "tennis_board", "templates", "static"
        ),
    )

    logger.info(
        "Static files path: %s",
        os.path.join(os.path.dirname(__file__), "tennis_board", "templates", "static"),
    )
    server = create_server(app, port=8001, url_prefix="/", host="127.0.0.1")

    logger.info("Server starting on port 8001...")
    server.run()
