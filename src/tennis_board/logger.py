import logging

from tennis_board.config import settings


def setup_logger():
    logging.basicConfig(
        level=settings.logger_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
