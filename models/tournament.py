from tinydb import TinyDB, where
from models.player import Player

"""Docstring."""

class Tournament:
    """Tournament"""

    dbtournament = TinyDB('tournaments.json', indent=4)

    def __init__(self, tournament_name, tournament_location, tournament_time_keeper, tournament_description, tournament_date):
        self.tournament_name = tournament_name
        self.tournament_location = tournament_location
        self.tournament_date = tournament_date
        self.tournament_time_keeper = tournament_time_keeper
        self.tournament_description = tournament_description

    def save_tournament(self):

        serialized_tournament = {
            'tournament_name': self.tournament_name,
            'tournament_location': self.tournament_location,
            'tournament_date': self.tournament_date,
            'tournament_time_keeper': self.tournament_time_keeper,
            'tournament_description': self.tournament_description
        }

        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournaments_table.insert(serialized_tournament) 