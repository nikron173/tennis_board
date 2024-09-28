from uuid import UUID

from tennis_board.dto.player import PlayerDto


class MatchCreate:
    def __init__(
        self,
        uuid: UUID,
        player_one_id: int,
        player_two_id: int,
        player_winner_id: int,
        score: str,
    ) -> None:
        self.uuid = uuid
        self.player_one_id = player_one_id
        self.player_two_id = player_two_id
        self.player_winner_id = player_winner_id
        self.score = score


class MatchDto:
    def __init__(
        self,
        match_uuid: UUID,
        player_one: PlayerDto,
        player_two: PlayerDto,
        winner: PlayerDto,
        score: str,
    ) -> None:
        self.match_uuid = match_uuid
        self.player_one = player_one
        self.player_two = player_two
        self.winner = winner
        self.score = score
