from tinydb import TinyDB


class Player:
    """Player."""

    dbplayer = TinyDB("players.json", indent=4)

    def __init__(
        self, player_name, player_first_name, player_date_of_birth, player_gender
    ):
        """Initialize a player."""
        self.player_name = player_name
        self.player_first_name = player_first_name
        self.player_date_of_birth = player_date_of_birth
        self.player_gender = player_gender

    def save_player(self):
        """Serialize a player to add it in the database."""

        serialized_player = {
            "player_name": self.player_name,
            "player_first_name": self.player_first_name,
            "player_date_of_birth": self.player_date_of_birth,
            "player_gender": self.player_gender,
        }

        players_table = Player.dbplayer.table("Players")
        players_table.insert(serialized_player)
