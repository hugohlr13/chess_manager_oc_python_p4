"""Docstring."""

class Player:
    """Docstring."""

    def __init__(self, player_surname, player_first_name, player_date_of_birth, player_gender, player_ranking, player_points):
        self.player_surname = player_surname
        self.player_first_name = player_first_name
        self.player_date_of_birth = player_date_of_birth
        self.player_id = player_date_of_birth + player_surname + player_first_name + player_gender 
        self.player_gender = player_gender
        self.player_ranking = player_ranking
        self.player_points = player_points
