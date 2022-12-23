from tinydb import TinyDB

"""Docstring."""

class Player:
    """Docstring."""

    dbplayer = TinyDB('players.json', indent=4)

    def __init__(self, player_name, player_first_name, player_date_of_birth, player_gender):
        self.player_name = player_name
        self.player_first_name = player_first_name
        self.player_date_of_birth = player_date_of_birth
        self.player_gender = player_gender
        self.get_player_view = GetPlayerView()


    def save_player(self):

        serialized_player = {
            'player_name': self.player_name,
            'player_first_name': self.player_first_name,
            'player_date_of_birth':self.player_date_of_birth,
            'player_gender': self.player_gender,
        }

        players_table = Player.dbplayer.table("Players")
        players_table.insert(serialized_player)
