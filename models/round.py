"""Docstring."""

class Round:
    """Round"""

    def __init__(self, round_name, round_start_date, round_start_time, round_end_date, round_end_time ):
        self.id_round = round_start_date + round_start_time + round_name
        self.matches = []
        self.round_name = round_name
        self.round_start_date : round_start_date
        self.round_start_time = round_start_time
        self.round_end_date = round_end_date
        self.round_end_time = round_end_time
