from views.base import MainMenuView
from views.base import NewTournamentView
from views.base import NewPlayerView
from views.base import AddPlayerTournamentView
from utils.menus import Menu
from models.tournament import Tournament
from models.player import Player
import datetime
from tinydb import TinyDB
from tinydb import Query

class ApplicationController:

    def __init__(self):
        self.controller = None

    def start(self):
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller.run()
            

class MainMenuController:

    def __init__(self):
        self.menu = Menu()
        self.view = MainMenuView(self.menu)

    def run(self):
        # 1. Construire un menu
        self.menu.add("auto", "créer un nouveau tournoi", NewTournamentController())
        self.menu.add("auto", "créer un profil joueur", NewPlayerController())
        self.menu.add("auto", "ajouter un joueur à un tournoi", AddPlayerTournamentController())
        self.menu.add("auto", "commencer le tournoi", StartTournamentController())
        self.menu.add("auto", "sauvegarder un tournoi en cours", SavePlayingTournamentController())
        self.menu.add("auto", "reprendre un tournoi en cours", OngoingTournamentController())
        self.menu.add("auto", "cloturer le tournoi", EndTournamentController())
        self.menu.add("auto", "actualiser le classement des joueurs après la fin d'un tournoi", UpdatePlayerRankingController())
        self.menu.add("auto", "modifier le classement des joueurs", EditPlayerRankingController())
        self.menu.add("auto", "afficher les rapports", DisplayListController())
        self.menu.add("auto", "quitter le gestionnaire de tournois d'échec.", ExitController())

        # 2. Demander à la vue d'afficher le menu et de collecter la réponse de l'utilisateur
        user_choice = self.view.get_user_choice()

        # 3. Retourner le controller associé au choix de l'utilisateur au contrôleur principal
        return user_choice.handler

class NewTournamentController:

    def __init__(self):
        self.menu = Menu()
        self.new_tournament_view = NewTournamentView()

    def create_tournament(self):
        print("dans le controleur de création de tournoi")
        tournament_datas = self.new_tournament_view.input_to_create_tournament()
        today_date = datetime.datetime.today()
        tournament_date = today_date.strftime("%d%m%Y")
        tournament_datas.append(tournament_date)
        print(tournament_datas)
        tournament = Tournament(*tournament_datas)
        tournament.save_tournament()

        return tournament

    def run(self):
        self.create_tournament()
        return MainMenuController()

class NewPlayerController:

    def __init__(self):
        self.menu = Menu()
        self.new_player_view = NewPlayerView()

    def create_player(self):
        print("dans le controleur de création de joueur")
        player_datas = self.new_player_view.input_to_create_player()
        print(player_datas)
        player = Player(*player_datas)
        player.save_player()

    def run(self):
        self.create_player()
        return MainMenuController()


class AddPlayerTournamentController:

    dbplayer_tournament = TinyDB('players_tournaments.json', indent=4)

    def __init__(self):
        self.add_player_tournament_view = AddPlayerTournamentView()

    def load_tournament_to_add_player(self):
        tournament_id = self.add_player_tournament_view.input_to_add_player_tournament_id()
        Tournament_query = Query()
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournament_to_find = tournaments_table.search(Tournament_query.tournament_id == tournament_id)
        if tournament_to_find:
            print(tournament_id)

        return tournament_id
    
    def add_player_tournament(self):
        tournament_id = self.load_tournament_to_add_player()
        print("\ndans le controleur d'ajout de joueur à un tournoi")
        player_id = self.add_player_tournament_view.input_to_add_player_id_tournament()
        User = Query()
        players_table = Player.dbplayer.table("Players")
        player_to_find = players_table.search(User.player_id == player_id)
        if player_to_find:
            print(player_id)
        else:
            print("L'Id du joueur n'est pas dans la base de données.")
        player_tournament_id = tournament_id + player_id
        print(player_tournament_id)

        return player_tournament_id

    def save_player_tournament_id(self):

        serialized_player_tournament = {
            'player_tournament_id': self.add_player_tournament(),
        }

        players_tournaments_table = AddPlayerTournamentController.dbplayer_tournament.table("Player_Tournaments")
        players_tournaments_table.insert(serialized_player_tournament)

    def run(self):
        self.save_player_tournament_id()
        return MainMenuController()

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
