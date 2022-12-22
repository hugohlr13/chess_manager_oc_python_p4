from tinydb import TinyDB


class Round:
    """Round"""

    dbround = TinyDB('rounds.json', indent=4)

    def __init__(self, round_name):
        self.round_name = round_name

    def save_round(self):

        serialized_round = {
            'round_name': self.round_name,
        }

        rounds_table = Round.dbround.table("Rounds")
        rounds_table.insert(serialized_round)
