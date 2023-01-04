class MainMenuView:

    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        print("\nBienvenue dans le gestionnaire de tournois d'échec.")
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")
        print()

    def get_user_choice(self):
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

    def input_to_create_tournament(self):
        tournament_datas = []

        tournament_name = input("\nNom du tournoi : ")
        tournament_location = input("\nLieu du tournoi : ")
        while True:
            tournament_time_keeper = input(
                "\nChoisissez le contrôle du temps entre 1, 2 ou 3 :\n" +
                "1 - bullet\n" +
                "2 - blitz\n" +
                "3 - coup rapide\n")
            if tournament_time_keeper == "1":
                tournament_time_keeper = "bullet"
                break
            elif tournament_time_keeper == "2":
                tournament_time_keeper = "blitz"
                break
            elif tournament_time_keeper == "3":
                tournament_time_keeper = "coup rapide"
                break
            else:
                continue
        tournament_description = input("\nDescription du tournoi: ")

        tournament_datas.append(tournament_name)
        tournament_datas.append(tournament_location)
        tournament_datas.append(tournament_time_keeper)
        tournament_datas.append(tournament_description)

        return tournament_datas


class NewPlayerView:

    def input_to_create_player(self):
        player_datas = []

        player_name = input("\nNom du joueur : ")
        player_first_name = input("\nPrénom du joueur : ")
        player_date_of_birth = input("\nDate de naissance (jjmmaaaa) : ")
        while True:
            player_gender = input(
                "\nChoisissez le genre du joueur :\n" +
                "H - Homme\n" +
                "F - Femme\n" +
                "A - Autre\n")
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

    def input_to_create_round(self):
        round_name = input("\nNom du round : ")


        return round_name


class GetPlayerView:

    def input_to_get_player(self):
        player_name = input("\nNom du joueur : ")
        return player_name


class GetTournamentView:

    def input_to_get_tournament(self):
        tournament_name = input("\nNom du tournoi : ")
        return tournament_name


class GetRoundView:

    def input_to_get_round(self):
        round_name = input("\nNom du round : ")
        return round_name


class GetMatchView:
    
    def input_to_get_match(self):
        match_id = int(input("\nId du match :"))
        return match_id


class AddMatchResultView:
    
    def input_to_add_match_result_score_A(self):
        score_A = float(input("\nScore du joueur A (0, 0.5 ou 1) :"))
        return score_A


    def input_to_add_match_result_score_B(self):
        score_B = float(input("\nScore du joueur B (0, 0.5 ou 1) :"))
        return score_B
 