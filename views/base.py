class MainMenuView:
    """View to manage the home menu."""

    def __init__(self, menu):
        """Initialize the view to manage the home menu"""
        self.menu = menu

    def _display_menu(self):
        """Display the home menu"""
        print("\nBienvenue dans le gestionnaire de tournois d'échec.")
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")
        print()

    def get_user_choice(self):
        """Ask user choice"""
        while True:
            # afficher le menu à l'utilisateur
            self._display_menu()
            # demander à l'utilisateur de faire un choix
            choice = input(">>")
            # valider le choix de l'utilisateur
            if choice in self.menu:
                # retourner le choix de l'utilisateur
                return self.menu[choice]


class NewTournamentView:
    """View to create a tournament"""

    def input_to_create_tournament(self):
        """Ask user tournament datas"""
        tournament_datas = []

        tournament_name = input("\nNom du tournoi : ")
        tournament_location = input("\nLieu du tournoi : ")
        while True:
            tournament_type = input(
                "\nChoisissez le contrôle du temps entre 1, 2 ou 3 :\n"
                + "1 - bullet\n"
                + "2 - blitz\n"
                + "3 - coup rapide\n"
            )
            if tournament_type == "1":
                tournament_type = "bullet"
                break
            elif tournament_type == "2":
                tournament_type = "blitz"
                break
            elif tournament_type == "3":
                tournament_type = "coup rapide"
                break
            else:
                continue
        tournament_description = input("\nDescription du tournoi: ")

        tournament_datas.append(tournament_name)
        tournament_datas.append(tournament_location)
        tournament_datas.append(tournament_type)
        tournament_datas.append(tournament_description)

        return tournament_datas


class NewPlayerView:
    """View to create player"""

    def input_to_create_player(self):
        """Ask user player datas"""
        player_datas = []

        player_name = input("\nNom du joueur : ")
        player_first_name = input("\nPrénom du joueur : ")
        player_date_of_birth = input("\nDate de naissance (jjmmaaaa) : ")
        while True:
            player_gender = input(
                "\nChoisissez le genre du joueur :\n"
                + "H - Homme\n"
                + "F - Femme\n"
                + "A - Autre\n"
            )
            if player_gender == "H":
                player_gender = "Homme"
                break
            elif player_gender == "F":
                player_gender = "Femme"
                break
            elif player_gender == "A":
                player_gender = "Autre"
                break
            else:
                continue

        player_datas.append(player_name)
        player_datas.append(player_first_name)
        player_datas.append(player_date_of_birth)
        player_datas.append(player_gender)

        return player_datas


class NewRoundView:
    """View to create a round"""

    def input_to_create_round(self):
        """Ask user round datas"""
        round_datas = []

        round_name = input("\nNom du round : ")
        round_number = int(input("\nNuméro du round : "))

        round_datas.append(round_name)
        round_datas.append(round_number)

        return round_datas


class GetPlayerView:
    """View to get a player"""

    def input_to_get_player(self):
        """Ask user player data"""
        player_name = input("\nNom du joueur : ")
        return player_name


class GetTournamentView:
    """View to get a tournament"""

    def input_to_get_tournament(self):
        """Ask user tournament data"""
        tournament_name = input("\nNom du tournoi : ")
        return tournament_name


class GetRoundView:
    """View to get a round"""

    def input_to_get_round(self):
        """Ask user round data"""
        round_number = int(input("\nNuméro du round : "))
        return round_number


class GetMatchView:
    """View to get a match"""

    def input_to_get_match(self):
        """Ask user match data"""
        match_id = int(input("\nId du match :"))
        return match_id


class AddMatchResultView:
    """View to add match result"""

    def input_to_add_match_result_score_A(self):
        """Ask user score player A"""
        score_A = float(input("\nScore du joueur A (0, 0.5 ou 1) :"))
        return score_A

    def input_to_add_match_result_score_B(self):
        """Ask user score player B"""
        score_B = float(input("\nScore du joueur B (0, 0.5 ou 1) :"))
        return score_B


class ReportView:
    """View to display report"""

    def display_report(self, datas):
        print("\n")
        for data in datas:
            print(data)
        print("\n")
