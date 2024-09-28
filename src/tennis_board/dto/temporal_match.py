from uuid import uuid4


class TemporalMatch:
    def __init__(
        self,
        player_one_name: str,
        player_two_name: str,
    ) -> None:
        self.uuid = uuid4()
        self.player_one = Score(player_one_name)
        self.player_two = Score(player_two_name)
        self.player_one_id = None
        self.player_two_id = None
        self.player_winner_id = None

    def set_player_one_id(self, player_id: int):
        self.player_one_id = player_id

    def set_player_two_id(self, player_id: int):
        self.player_two_id = player_id

    def set_player_winner_id(self, player_id: int):
        self.player_winner_id = player_id


class Score:
    def __init__(self, player_name: str) -> None:
        self.name = player_name
        self.point = 0
        self.game = 0
        self.set = 0
        self.tie_break = False

    def add_point(self):
        self.point += 1

    def add_game(self):
        self.game += 1

    def add_set(self):
        self.set += 1

    def check_win_game(self, comparative_score) -> bool:
        if self.point > 3 and comparative_score.point < 3:
            return True
        if (
            self.point > 3
            and comparative_score.point >= 3
            and (self.point - comparative_score.point) > 1
        ):
            return True
        return False

    def check_win(self, comparative_score) -> bool:
        if self.game > 5 and (self.game - comparative_score.game) > 1:
            return True
        if self.game == 6 and comparative_score.game == 6:
            self.tie_break = True
            comparative_score.tie_break = True
        return False

    def check_win_tie_break(self, comparative_score) -> bool:
        if self.point > 6 and (self.point - comparative_score.point) > 1:
            return True
        return False
