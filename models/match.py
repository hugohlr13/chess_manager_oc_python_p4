from tinydb import TinyDB


class Match:
    """Match"""

    dbmatch = TinyDB("matches.json", indent=4)

    def __init__(self, round_id, player_A, player_B):
        """Initialize a match."""
        self.round_id = round_id
        self.player_A = player_A
        self.player_B = player_B
        self.score_A = None
        self.score_B = None

    def save_match(self):
        """Serialize a match to add it in the database."""

        serialized_match = {
            "round_id": self.round_id,
            "player_A": self.player_A,
            "score_A": self.score_A,
            "player_B": self.player_B,
            "score_B": self.score_B,
        }

        matches_table = Match.dbmatch.table("Matches")
        match_id = matches_table.insert(serialized_match)

        return match_id
