from tinydb import TinyDB

class Round:
    """Round"""

    dbround = TinyDB('rounds.json', indent=4)

    def __init__(self, round_name, round_start_date_time, round_end_date_time):
        self.round_name = round_name
        self.round_start_date_time : round_start_date_time
        self.round_end_date_time = round_end_date_time
    
    def save_round(self):

        serialized_round = {
            'round_name': self.round_name,
            'round_start_date_time': self.round_start_date_time,
            'round_end_date_time':self.round_end_date_time,
        }

        roundss_table = Round.dbround.table("Rounds")
        roundss_table.insert(serialized_round)