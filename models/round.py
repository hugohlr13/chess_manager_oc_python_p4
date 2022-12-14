from tinydb import TinyDB


class Round:
    """Round"""

    dbround = TinyDB("rounds.json", indent=4)

    def __init__(self, round_name, round_number, tournament_id):
        """Initialize a round."""
        self.round_name = round_name
        self.round_number = round_number
        self.tournament_id = tournament_id
        self.round_start_date_time = None
        self.round_end_date_time = None

    def save_round(self):
        """Serialize a round to add it in the database."""

        serialized_round = {
            "round_name": self.round_name,
            "round_number": self.round_number,
            "tournament_id": self.tournament_id,
            "round_start_date_time": self.round_start_date_time,
            "round_end_date_time": self.round_end_date_time,
        }

        rounds_table = Round.dbround.table("Rounds")
        rounds_table.insert(serialized_round)
