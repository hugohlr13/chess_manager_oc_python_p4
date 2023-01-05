from tinydb import TinyDB

"""Docstring."""


class Tournament:
    """Tournament"""

    dbtournament = TinyDB("tournaments.json", indent=4)

    def __init__(
        self, tournament_name, tournament_location, tournament_type, tournament_description, tournament_start
    ):
        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_start = tournament_start
        self.tournament_end = None
        self.tournament_type = tournament_type
        self.tournament_description = tournament_description

    def save_tournament(self):

        serialized_tournament = {
            "tournament_name": self.tournament_name,
            "tournament_location": self.tournament_location,
            "tournament_start": self.tournament_start,
            "tournament_end": self.tournament_end,
            "tournament_type": self.tournament_type,
            "tournament_description": self.tournament_description,
        }

        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournaments_table.insert(serialized_tournament)
