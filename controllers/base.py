from views.base import MainMenuView
from utils.menus import Menu

class ApplicationController:

    def __init__(self):
        self.controller = None

    def start(self):
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller()
            

class MainMenuController:

    def __init__(self):
        self.menu = Menu()
        self.view = MainMenuView(self.menu)

    def __call__(self):
        # 1. Construire un menu
        self.menu.add("auto", "créer un nouveau tournoi", NewTournamentController())
        self.menu.add("auto", "ajouter un joueur à un tournoi", AddPlayerTournamentController())
        self.menu.add("auto", "commencer le tournoi", StartTournamentController())
        self.menu.add("auto", "sauvegarder un tournoi en cours", SavePlayingTournamentController())
        self.menu.add("auto", "reprendre un tournoi en cours", OngoingTournamentController())
        self.menu.add("auto", "cloturer le tournoi", EndTournamentController())
        self.menu.add("auto", "actualiser le classement des joueurs après la fin d'un tournoi", UpdatePlayerRankingController())
        self.menu.add("auto", "modifier le classement des joueurs", EditPlayerRankingController())
        self.menu.add("auto", "afficher les rapports", DisplayListController())
        self.menu.add("exit", "quitter le controller", ExitController())

        # 2. Demander à la vue d'afficher le menu et de collecter la réponse de l'utilisateur
        user_choice = self.view.get_user_choice()

        # 3. Retourner le controller associé au choix de l'utilisateur au contrôleur principal
        return user_choice.handler

class NewTournamentController:
    def __call__(self):
        print("dans le controleur de création de tournoi")

class AddPlayerTournamentController:
    pass

class StartTournamentController:
    pass

class SavePlayingTournamentController:
    pass

class OngoingTournamentController:
    pass

class EndTournamentController:
    pass

class UpdatePlayerRankingController:
    pass

class EditPlayerRankingController:
    pass

class DisplayListController:
    pass

class ExitController:
    pass


#Créer un nouveau tournoi
#Ajouter un nouveau joueur x8
#Générer les paires de joueur
#Entrer les résultats du premier tour
#Faire tous les tours 
#Cloturer le tournoi