from tinydb import TinyDB


class Round:
    """Round"""

    dbround = TinyDB('rounds.json', indent=4)

    def __init__(self, round_name, tournament_id):
        self.round_name = round_name
        self.tournament_id = tournament_id
        self.round_start_date_time = None
        self.round_end_date_time = None

    def save_round(self):

        serialized_round = {
            'round_name': self.round_name,
            'tournament_id': self.tournament_id,
            'round_start_date_time': self.round_start_date_time,
            'round_end_date_time': self.round_end_date_time,
        }

        rounds_table = Round.dbround.table("Rounds")
        rounds_table.insert(serialized_round)
