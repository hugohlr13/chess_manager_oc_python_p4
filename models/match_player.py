from tinydb import TinyDB


class Player_A:

    dbmatch_player = TinyDB("match_player.json", indent=4)

    def __init__(self, player_A, match_id):

        self.player_A = player_A
        self.match_id = match_id

    def save_match_player_id_A(self):

        serialized_match_player = {
            "player_id": self.player_A,
            "match_id": self.match_id,
        }

        match_player_table = Player_A.dbmatch_player.table("Match_Player")
        match_player_table.insert(serialized_match_player)


class Player_B:
    def __init__(self, player_B, match_id):

        self.player_B = player_B
        self.match_id = match_id

    def save_match_player_id_B(self):

        serialized_match_player = {
            "player_id": self.player_B,
            "match_id": self.match_id,
        }
        match_player_table = Player_A.dbmatch_player.table("Match_Player")
        match_player_table.insert(serialized_match_player)
