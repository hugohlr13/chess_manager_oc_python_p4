class MainMenuView:

    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        print("Bienvenue dans le gestionnaire de tournois d'échec.")
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

    def prompt_to_create_tournament(self):
        tournament_datas = []

        tournament_name = input("\nNom du tournoi: ")
        tournament_location = input("\nLieu du tournoi: ")
        while True:
            tournament_time_keeper = input(
                "\nChoisissez le contrôle du temps entre 1, 2 ou 3:\n" +
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
