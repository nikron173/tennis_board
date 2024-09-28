from typing import List

# from tennis_board.dto.match import MatchDto


class PlayerCreate:
    def __init__(self, name: str) -> None:
        self.name = name


class PlayerDto(PlayerCreate):
    def __init__(self, player_id: int, name: str) -> None:
        super().__init__(name)
        self.player_id = player_id


class PlayerMatchesDto(PlayerDto):
    def __init__(
        self,
        player_id: int,
        name: str,
        matches: List,
        matches_winner: List,
    ) -> None:
        super().__init__(player_id, name)
        self.matches = matches
        self.matches_winner = matches_winner
