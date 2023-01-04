from views.base import MainMenuView
from views.base import NewTournamentView
from views.base import NewPlayerView
from views.base import GetPlayerView
from views.base import GetTournamentView
from views.base import NewRoundView
from views.base import GetRoundView
from views.base import GetMatchView
from views.base import AddMatchResultView
from utils.menus import Menu
from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match
from models.match_player import Player_A, Player_B
import datetime
import random
from tinydb import TinyDB
from tinydb import Query
from tinydb.operations import add


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
        self.menu.add("auto", "commencer un round", RoundTournamentController())
        self.menu.add("auto", "ajouter les résultats d'un match", AddMatchResultTournamentController())
        self.menu.add("auto", "ajouter un round au tournoi", AddRoundTournamentController())
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
        tournament_name = tournament_datas[0]

        return tournament_name

    def create_rounds(self):
        tournament_name = self.create_tournament()
        Tournament_query = Query()
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournament_to_find = tournaments_table.get(Tournament_query.tournament_name == tournament_name)
        tournament_id = tournament_to_find.doc_id
        rounds_name = ["Round 1", "Round 2", "Round 3", "Round 4"]
        rounds_number = [1, 2, 3, 4]
        for round in range(0,4,1):
            round_name = rounds_name[round]
            round_number = rounds_number[round]
            round = Round(round_name, round_number, tournament_id)
            round.save_round()

    def run(self):
        self.create_rounds()
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
        print("\ndans le controleur pour récupérer un tournoi")
        tournament_name = self.get_tournament_view.input_to_get_tournament()
        Tournament_query = Query()
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournament_to_find = tournaments_table.get(Tournament_query.tournament_name == tournament_name)
        tournament_id = tournament_to_find.doc_id

        return tournament_id

    def get_player(self):
        print("\ndans le controleur pour récupérer un joueur")
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
            'player_points': float(0)
        }

        players_tournaments_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        players_tournaments_table.insert(serialized_tournament_player)

    def run(self):
        self.save_tournament_player_id()
        return MainMenuController()


class RoundTournamentController:

    def __init__(self):
        self.get_tournament = AddPlayerTournamentController()
        self.get_round_view = GetRoundView()

    def get_players_round(self):
        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        round_name = self.get_round_view.input_to_get_round()
        Round_query = Query()
        rounds_table = Round.dbround.table("Rounds")
        round_to_find = rounds_table.get(Round_query.round_name == round_name)
        round_id = round_to_find.doc_id
        players_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        Players = Query()
        players_searched = players_table.search(Players.tournament_id == tournament_id)
        if round_name == "Round1":
            players_id = []
            for player in players_searched:
                player_id = player['player_id']
                players_id.append(player_id)                
            random.shuffle(players_id)
            print(players_id)
            for player in range(0,7,2):
                player_A = int(players_id[player])
                player_B = int(players_id[player+1])
                match = Match(round_id, player_A, player_B)
                match_id = match.save_match()
                match_player_A = Player_A(player_A, match_id)
                match_player_A.save_match_player_id_A()
                match_player_B = Player_B(player_B, match_id)
                match_player_B.save_match_player_id_B()
        else:
            sorted_players_searched = sorted(players_searched, key=lambda d: d['player_points'], reverse=True)
            print(sorted_players_searched)
            players_id = []
            for player in sorted_players_searched:
                player_id = player['player_id']
                players_id.append(player_id)
            print(players_id)
            for player in range(0,7,2):
                player_A = int(players_id[player])
                player_B = int(players_id[player+1])
                match = Match(round_id, player_A, player_B)
                match_id = match.save_match()
                match_player_A = Player_A(player_A, match_id)
                match_player_A.save_match_player_id_A()
                match_player_B = Player_B(player_B, match_id)
                match_player_B.save_match_player_id_B()

    def run(self):
        self.get_players_round()
        return MainMenuController()


class AddMatchResultTournamentController:

    def __init__(self):
        self.get_match_view = GetMatchView()
        self.add_result_match_view = AddMatchResultView()
        self.get_tournament = AddPlayerTournamentController()

    def get_match(self):
        match_id = self.get_match_view.input_to_get_match()
        matches_table = Match.dbmatch.table("Matches")
        match_datas = matches_table.get(doc_id=match_id)
        print(match_datas) 

    def add_result(self):
        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        match_id = self.get_match_view.input_to_get_match()
        print(match_id)
        score_A = self.add_result_match_view.input_to_add_match_result_score_A()
        score_B = self.add_result_match_view.input_to_add_match_result_score_B()
        print(type(score_A))
        matches_table = Match.dbmatch.table("Matches")
        match_datas = matches_table.update({'score_A': score_A, 'score_B': score_B }, doc_ids=[match_id])
        print(match_datas)
        match_players_infos = matches_table.get(doc_id=match_id)
        print(match_players_infos)
        player_id = match_players_infos['player_A']  
        print(player_id)
        players_tournaments_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        Players = Query()
        tournament_player_searched = players_tournaments_table.search((Players.tournament_id == tournament_id) & (Players.player_id == player_id))
        print(tournament_player_searched)
        tournament_player_update = players_tournaments_table.update(add('player_points', score_A), ((Players.tournament_id == tournament_id) & (Players.player_id == player_id)))
        print(tournament_player_update)
        player_id = match_players_infos ['player_B']
        print(player_id)
        players_tournaments_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        Players = Query()
        tournament_player_searched = players_tournaments_table.search((Players.tournament_id == tournament_id) & (Players.player_id == player_id))
        print(tournament_player_searched)
        tournament_player_update = players_tournaments_table.update(add('player_points', score_B), ((Players.tournament_id == tournament_id) & (Players.player_id == player_id)))
        print(tournament_player_update)

    def run(self):
        self.add_result()
        return MainMenuController()


class AddRoundTournamentController:

    def __init__(self):
        self.get_tournament = AddPlayerTournamentController()
        self.new_round_view = NewRoundView()
   
    def create_round(self):
        print("dans le controleur pour créer un round")
        
        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        round_name = self.new_round_view.input_to_create_round()
        round = Round(round_name, tournament_id)
        round.save_round()

    def run(self):
        self.create_round()
        return MainMenuController()


class EndTournamentController:
    pass

class DisplayListController:

    def __init__(self):
        self.menu = Menu()
        self.view = MainMenuView(self.menu)

    def run(self):
        # 1. Construire un menu
        self.menu.add("auto", "afficher la liste de tous les joueurs par ordre alphabétique", PlayerListDisplayController())
        self.menu.add("auto", "afficher la liste de tous les tournois", TournamentListDisplayController())
        self.menu.add("auto", "afficher la date d'un tournoi donné", TournamentDateDisplayController())
        self.menu.add("auto", "afficher la liste des joueurs d'un tournoi", TournamentPlayerDisplayController())
        self.menu.add("auto", "afficher la liste des tours et des matchs du tour", RoundMatchListDisplayController())

        # 2. Demander à la vue d'afficher le menu et de collecter la réponse de l'utilisateur
        user_choice = self.view.get_user_choice()

        # 3. Retourner le controller associé au choix de l'utilisateur au contrôleur principal
        return user_choice.handler

class PlayerListDisplayController:

    def __init__(self):
        pass

    def get_all_players(self):
        players_table = Player.dbplayer.table("Players")
        all_players = []
        for player in players_table:
            player_name = player['player_name']
            all_players.append(player_name)
        sorted_all_players = sorted(all_players)
        print(sorted_all_players)

    def run(self):
        self.get_all_players()
        return MainMenuController()

class TournamentListDisplayController:

    def __init__(self):
        pass

    def get_all_players(self):
        tournament_table = Tournament.dbtournament.table("Tournaments")
        all_tournaments = []
        for tournament in tournament_table:
            tournament_name = tournament['tournament_name']
            all_tournaments.append(tournament_name)
        sorted_all_tournaments = sorted(all_tournaments)
        print(sorted_all_tournaments)

    def run(self):
        self.get_all_players()
        return MainMenuController()

class TournamentDateDisplayController:

    def __init__(self):
        self.get_tournament_name_view = GetTournamentView()
        pass

    def get_tournament_date(self):
        tournament_name = self.get_tournament_name_view.input_to_get_tournament()
        tournament_table = Tournament.dbtournament.table("Tournaments")
        Tournaments = Query()
        tournament_searched = tournament_table.search(Tournaments.tournament_name == tournament_name)
        print(tournament_name)
        tournament_date = tournament_searched[0]["tournament_date"]
        print(tournament_date)

    def run(self):
        self.get_tournament_date()
        return MainMenuController()

class TournamentPlayerDisplayController:

    def __init__(self):
        self.get_tournament = AddPlayerTournamentController()

    def get_tournament_players(self):
        tournament_id = self.get_tournament.get_tournament()
        tournament_players_id_table = AddPlayerTournamentController.dbplayer_tournament.table("Tournaments_Players")
        Players = Query()
        players_searched = tournament_players_id_table.search(Players.tournament_id == tournament_id)
        players_id = []
        for player in players_searched:
            player_id = player['player_id']
            players_id.append(player_id)
        tournament_players_name = []
        for player_id in players_id:
            tournament_players_name_table = Player.dbplayer.table("Players")
            player_searched = tournament_players_name_table.get(doc_id=player_id)
            player_found = player_searched["player_name"]
            tournament_players_name.append(player_found)
        sorted_tournament_players_name = sorted(tournament_players_name)
        print(sorted_tournament_players_name)       

    def run(self):
        self.get_tournament_players()
        return MainMenuController()

class RoundMatchListDisplayController():

    def __init__(self):
        self.get_tournament = AddPlayerTournamentController()

    def get_rounds_matches(self):
        tournament_id = self.get_tournament.get_tournament()
        rounds_table = Round.dbround.table("Rounds")
        Rounds = Query()
        rounds_searched = rounds_table.search(Rounds.tournament_id == tournament_id)
        rounds_list = []
        for round in rounds_searched:
            round_name = round['round_name']
            rounds_list.append(round_name)
        print(rounds_list)
        matches_list = []
        for round_name in rounds_list:
            Rounds = Query()
            round_searched = rounds_table.get(Rounds.round_name == round_name)
            round_id = round_searched.doc_id
            matches_table = Match.dbmatch.table("Matches")
            Matches = Query()
            matches_searched = matches_table.search(Matches.round_id == round_id)
            matches_list.append(matches_searched)
        print(matches_list)

    def run(self):
        self.get_rounds_matches()
        return MainMenuController()

class ExitController:

    def run(self):
        return None
