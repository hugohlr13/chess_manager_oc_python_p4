from views.base import MainMenuView
from views.base import NewTournamentView
from views.base import NewPlayerView
from views.base import GetPlayerView
from views.base import GetTournamentView
from views.base import CreateRoundView
from utils.menus import Menu
from models.tournament import Tournament
from models.player import Player
from models.round import Round
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

    dbplayer_tournament = TinyDB('tournaments_players.json', indent=4)

    def __init__(self):
        self.get_tournament_view = GetTournamentView()
        self.add_player_tournament_view = GetPlayerView()

    def get_tournament(self):
        tournament_name = self.get_tournament_view.input_to_get_tournament()
        Tournament_query = Query()
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournament_to_find = tournaments_table.get(Tournament_query.tournament_name == tournament_name)
        tournament_id = tournament_to_find.doc_id
        if tournament_to_find:
            print(tournament_to_find)

        return tournament_id

    def get_player(self):
        player_name = self.add_player_tournament_view.input_to_get_player()
        User = Query()
        players_table = Player.dbplayer.table("Players")
        player_to_find = players_table.get(User.player_name == player_name)
        if player_to_find:
            print(player_to_find)           
        else:
            print("L'Id du joueur n'est pas dans la base de données.")
        player_id = player_to_find.doc_id

        return player_id
    
    def save_tournament_player_id(self):
        print("\ndans le controleur d'ajout de joueur à un tournoi")

        serialized_tournament_player = {
            'tournament_id': self.get_tournament(),
            'player_id': self.get_player(),
        }

        players_tournaments_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        players_tournaments_table.insert(serialized_tournament_player)

    def run(self):
        self.save_tournament_player_id()
        return MainMenuController()


class StartTournamentController:

    def __init__(self):
        self.create_round_view = CreateRoundView()
        self.get_tournament = AddPlayerTournamentController()
   
    def get_players(self):
        print("dans le controleur pour démarrer le tournoi (joueurs)")
        
        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        tournament_players_id = []
        players_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        for player_to_find in players_table:
            Players = Query()
            player_to_find = players_table.get(Players.tournament_id == tournament_id)
            if player_to_find:
                print(player_to_find)
            else:
                print("L'Id du tournoi_joueur n'est pas dans la base de données.")
            player_to_find = player_to_find.doc_id
            print(player_to_find)
            tournament_players_id.append(player_to_find)

        print(tournament_players_id)
        
    def get_rounds(self):
        print("dans le controleur pour démarrer le tournoi (rounds)")

        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        round_name = self.create_round_view.input_to_create_round()
        round = Round(round_name, tournament_id)
        round.save_round()
        

    def run(self):
        self.get_players()
        self.get_rounds()
        return MainMenuController()

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
