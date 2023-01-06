"""Module to define controllers."""

import datetime
import random

from tinydb import Query, TinyDB
from tinydb.operations import add

from models.match import Match
from models.match_player import Player_A, Player_B
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from utils.menus import Menu
from views.base import (AddMatchResultView, GetMatchView, GetPlayerView,
                        GetRoundView, GetTournamentView, MainMenuView,
                        NewPlayerView, NewRoundView, NewTournamentView)


class ApplicationController:
    """Launch the application by starting a home menu"""

    def __init__(self):
        """Initialize the application"""
        self.controller = None

    def start(self):
        """Starts the application with the home menu"""
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller.run()


class MainMenuController:
    """The menu allows the user to choose his actions."""

    def __init__(self):
        """Initialize the menu."""
        self.menu = Menu()
        self.view = MainMenuView(self.menu)

    def run(self):
        """Displays the home menu to the user."""
        # 1. Construire un menu
        self.menu.add("auto", "créer un nouveau tournoi", NewTournamentController())
        self.menu.add("auto", "créer un profil joueur", NewPlayerController())
        self.menu.add(
            "auto", "ajouter un joueur à un tournoi", AddPlayerTournamentController()
        )
        self.menu.add("auto", "commencer un round", RoundMatchTournamentController())
        self.menu.add(
            "auto",
            "ajouter les résultats d'un match",
            AddMatchResultTournamentController(),
        )
        self.menu.add(
            "auto", "ajouter un round au tournoi", AddRoundTournamentController()
        )
        self.menu.add(
            "auto", "clôturer un round/tournoi", EndRoundTournamentController()
        )
        self.menu.add("auto", "afficher les rapports", DisplayReportController())
        self.menu.add(
            "auto", "quitter le gestionnaire de tournois d'échec.", ExitController()
        )

        # 2. Demander à la vue d'afficher le menu et de collecter la réponse de l'utilisateur
        user_choice = self.view.get_user_choice()

        # 3. Retourner le controller associé au choix de l'utilisateur au contrôleur principal
        return user_choice.handler


class NewTournamentController:
    """Create a new tournament."""

    def __init__(self):
        """Initialize the creation of a tournament."""
        self.new_tournament_view = NewTournamentView()

    def create_tournament(self):
        """Create the tournament with the information requested from the user."""
        print("dans le controleur de création de tournoi")
        tournament_datas = self.new_tournament_view.input_to_create_tournament()
        today_date = datetime.datetime.today()
        tournament_start = today_date.strftime("%d%m%Y")
        tournament_datas.append(tournament_start)
        print(tournament_datas)
        tournament = Tournament(*tournament_datas)
        tournament.save_tournament()
        tournament_name = tournament_datas[0]

        return tournament_name

    def create_rounds(self):
        """Automatically created four rounds when creating a new tournament."""
        tournament_name = self.create_tournament()
        Tournament_query = Query()
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournament_to_find = tournaments_table.get(
            Tournament_query.tournament_name == tournament_name
        )
        tournament_id = tournament_to_find.doc_id
        rounds_name = ["Round 1", "Round 2", "Round 3", "Round 4"]
        rounds_number = [1, 2, 3, 4]
        for round in range(0, 4, 1):
            round_name = rounds_name[round]
            round_number = rounds_number[round]
            round = Round(round_name, round_number, tournament_id)
            round.save_round()

    def run(self):
        """Method to create the tournament and return to the home menu."""
        self.create_rounds()
        return MainMenuController()


class NewPlayerController:
    """Create a new player."""

    def __init__(self):
        """Initialize the creation of a tournament."""
        self.new_player_view = NewPlayerView()

    def create_player(self):
        """Create the player with the information requested from the user."""
        print("dans le controleur de création de joueur")
        player_datas = self.new_player_view.input_to_create_player()
        print(player_datas)
        player = Player(*player_datas)
        player.save_player()

    def run(self):
        """Method to create the player and return to the home menu."""
        self.create_player()
        return MainMenuController()


class AddPlayerTournamentController:
    """Add a player to a tournament."""

    dbplayer_tournament = TinyDB("tournaments_players.json", indent=4)

    def __init__(self):
        """Initialize the addition of a player to a tournament."""
        self.get_tournament_view = GetTournamentView()
        self.add_player_tournament_view = GetPlayerView()

    def get_tournament(self):
        """Retrieve the id of a tournament from the tournament name."""
        print("\ndans le controleur pour récupérer un tournoi")
        tournament_name = self.get_tournament_view.input_to_get_tournament()
        Tournament_query = Query()
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        tournament_to_find = tournaments_table.get(
            Tournament_query.tournament_name == tournament_name
        )
        tournament_id = tournament_to_find.doc_id

        return tournament_id

    def get_player(self):
        """Retrieve the id of a player from the player's name."""
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
        """Save the id of a player registered in a tournament."""
        print("\ndans le controleur d'ajout de joueur à un tournoi")

        serialized_tournament_player = {
            "tournament_id": self.get_tournament(),
            "player_id": self.get_player(),
            "player_points": float(0),
        }

        players_tournaments_table = (
            AddPlayerTournamentController.dbplayer_tournament.table(
                "Tournaments_Players"
            )
        )
        players_tournaments_table.insert(serialized_tournament_player)

    def run(self):
        """Method to create the player_tournament ID and return to the home menu."""

        self.save_tournament_player_id()
        return MainMenuController()


class RoundMatchTournamentController:
    """Create the matches of a round according to its number."""

    def __init__(self):
        """Initialize the creation of the matches of a round."""
        self.get_tournament = AddPlayerTournamentController()
        self.get_round_view = GetRoundView()

    def save_match(self, round_id, player_A, player_B):
        """Save the information of a match."""
        match = Match(round_id, player_A, player_B)
        match_id = match.save_match()
        match_player_A = Player_A(player_A, match_id)
        match_player_A.save_match_player_id_A()
        match_player_B = Player_B(player_B, match_id)
        match_player_B.save_match_player_id_B()

    def get_players_round(self):
        """Give the list of matches to be played by round."""
        tournament_id = self.get_tournament.get_tournament()
        round_number = self.get_round_view.input_to_get_round()
        rounds_table = Round.dbround.table("Rounds")
        Rounds = Query()
        round_to_find = rounds_table.get(
            (Rounds.tournament_id == tournament_id)
            & (Rounds.round_number == round_number)
        )
        round_id = round_to_find.doc_id
        today_date = datetime.datetime.today()
        round_start_date = today_date.strftime("%d%m%Y")
        round_data = rounds_table.update(
            {"round_start_date_time": round_start_date}, doc_ids=[round_id]
        )
        print(round_data)
        players_table = AddPlayerTournamentController.dbplayer_tournament.table(
            "Tournaments_Players"
        )
        Players = Query()
        players_searched = players_table.search(Players.tournament_id == tournament_id)
        if round_number == 1:
            players_id = []
            for player in players_searched:
                player_id = player["player_id"]
                players_id.append(player_id)
            random.shuffle(players_id)
            print(players_id)
            for player in range(0, 7, 2):
                player_A = int(players_id[player])
                player_B = int(players_id[player + 1])
                save_match = self.save_match(round_id, player_A, player_B)
                save_match
        else:
            sorted_players_searched = sorted(
                players_searched, key=lambda d: d["player_points"], reverse=True
            )
            print(sorted_players_searched)
            players_id = []
            for player in sorted_players_searched:
                player_id = player["player_id"]
                players_id.append(player_id)
            print(players_id)
            for player in range(0, 7, 2):
                player_A = int(players_id[player])
                player_B = int(players_id[player + 1])
                save_match = self.save_match(round_id, player_A, player_B)
                save_match

    def run(self):
        """Method to create matches for a round and return to the home menu."""
        self.get_players_round()
        return MainMenuController()


class AddMatchResultTournamentController:
    """Add by the user the result of a match."""

    def __init__(self):
        """Initialize the addition of a match result."""
        self.get_match_view = GetMatchView()
        self.add_result_match_view = AddMatchResultView()
        self.get_tournament = AddPlayerTournamentController()

    def get_match(self):
        """Displays the information of a match."""
        match_id = self.get_match_view.input_to_get_match()
        matches_table = Match.dbmatch.table("Matches")
        match_datas = matches_table.get(doc_id=match_id)
        print(match_datas)

    def add_result(self):
        """Add the result of a match."""
        tournament_id = self.get_tournament.get_tournament()
        match_id = self.get_match_view.input_to_get_match()
        score_A = self.add_result_match_view.input_to_add_match_result_score_A()
        score_B = self.add_result_match_view.input_to_add_match_result_score_B()
        matches_table = Match.dbmatch.table("Matches")
        match_datas = matches_table.update(
            {"score_A": score_A, "score_B": score_B}, doc_ids=[match_id]
        )
        match_datas
        match_players_infos = matches_table.get(doc_id=match_id)
        player_id = match_players_infos["player_A"]
        players_tournaments_table = (
            AddPlayerTournamentController.dbplayer_tournament.table(
                "Tournaments_Players"
            )
        )
        Players = Query()
        tournament_player_searched = players_tournaments_table.search(
            (Players.tournament_id == tournament_id) & (Players.player_id == player_id)
        )
        tournament_player_update = players_tournaments_table.update(
            add("player_points", score_A),
            (
                (Players.tournament_id == tournament_id)
                & (Players.player_id == player_id)
            ),
        )
        player_id = match_players_infos["player_B"]
        players_tournaments_table = (
            AddPlayerTournamentController.dbplayer_tournament.table(
                "Tournaments_Players"
            )
        )
        Players = Query()
        tournament_player_searched = players_tournaments_table.search(
            (Players.tournament_id == tournament_id) & (Players.player_id == player_id)
        )
        tournament_player_searched
        tournament_player_update = players_tournaments_table.update(
            add("player_points", score_B),
            (
                (Players.tournament_id == tournament_id)
                & (Players.player_id == player_id)
            ),
        )
        tournament_player_update

    def run(self):
        """Method to add the result of a match and return to the home menu."""
        self.add_result()
        return MainMenuController()


class AddRoundTournamentController:
    """Add a round to a tournament."""

    def __init__(self):
        """Initialize the addition of a round to a tournament."""
        self.get_tournament = AddPlayerTournamentController()
        self.new_round_view = NewRoundView()

    def create_round(self):
        """Add a round to a tournament."""
        print("dans le controleur pour créer un round")

        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        round_datas = self.new_round_view.input_to_create_round()
        print(round_datas)
        round_name = round_datas[0]
        round_number = round_datas[1]
        round = Round(round_name, round_number, tournament_id)
        round.save_round()

    def run(self):
        """Method to add a round to a tournament and return to the home menu."""
        self.create_round()
        return MainMenuController()


class EndRoundTournamentController:
    """Closing a round or tournament by launching a sub-menu."""

    def __init__(self):
        """Initialize the closing of a round or tournament."""
        self.menu = Menu()
        self.view = MainMenuView(self.menu)

    def run(self):
        """Method to launch the closing of a round or a tournament."""
        # 1. Construire un menu
        self.menu.add("auto", "clôturer un round", EndRoundController())
        self.menu.add("auto", "clôturer un tournoi", EndTournamentController())

        # 2. Demander à la vue d'afficher le menu et de collecter la réponse de l'utilisateur
        user_choice = self.view.get_user_choice()

        # 3. Retourner le controller associé au choix de l'utilisateur au contrôleur principal
        return user_choice.handler


class EndRoundController:
    """Closing a round."""

    def __init__(self):
        """Initialize the closing of a round."""
        self.get_tournament = AddPlayerTournamentController()
        self.get_round_view = GetRoundView()

    def end_round(self):
        """Closing a round"""
        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        round_number = self.get_round_view.input_to_get_round()
        rounds_table = Round.dbround.table("Rounds")
        Rounds = Query()
        round_to_find = rounds_table.get(
            (Rounds.tournament_id == tournament_id)
            & (Rounds.round_number == round_number)
        )
        print(round_to_find)
        round_id = round_to_find.doc_id
        print(round_id)
        today_date = datetime.datetime.today()
        round_end_date = today_date.strftime("%d%m%Y")
        round_data = rounds_table.update(
            {"round_end_date_time": round_end_date}, doc_ids=[round_id]
        )
        print(round_data)

    def run(self):
        """Method to close a round."""
        self.end_round()
        return MainMenuController()


class EndTournamentController:
    """Closing a tournament."""

    def __init__(self):
        """Initialize the closing of a tournament."""
        self.get_tournament = AddPlayerTournamentController()

    def end_tournament(self):
        """Closing a tournament"""
        tournament_id = self.get_tournament.get_tournament()
        print(tournament_id)
        tournaments_table = Tournament.dbtournament.table("Tournaments")
        today_date = datetime.datetime.today()
        tournament_end = today_date.strftime("%d%m%Y")
        tournament_data = tournaments_table.update(
            {"tournament_end": tournament_end}, doc_ids=[tournament_id]
        )
        print(tournament_data)

    def run(self):
        """Method to close a tournament."""
        self.end_tournament()
        return MainMenuController()


class DisplayReportController:
    """Displays reports"""

    def __init__(self):
        """Initialize the display of reports."""
        self.menu = Menu()
        self.view = MainMenuView(self.menu)

    def run(self):
        """Method to select the report to be displayed."""
        # 1. Construire un menu
        self.menu.add(
            "auto",
            "afficher la liste de tous les joueurs par ordre alphabétique",
            PlayerReportController(),
        )
        self.menu.add(
            "auto",
            "afficher la liste de tous les tournois",
            TournamentReportController(),
        )
        self.menu.add(
            "auto", "afficher les dates d'un tournoi", TournamentDateReportController()
        )
        self.menu.add(
            "auto",
            "afficher la liste des joueurs d'un tournoi",
            TournamentPlayerReportController(),
        )
        self.menu.add(
            "auto",
            "afficher la liste des tours et des matchs du tour",
            RoundMatchReportController(),
        )

        # 2. Demander à la vue d'afficher le menu et de collecter la réponse de l'utilisateur
        user_choice = self.view.get_user_choice()

        # 3. Retourner le controller associé au choix de l'utilisateur au contrôleur principal
        return user_choice.handler


class PlayerReportController:
    """Displays the player list report in alphabetical order."""

    def __init__(self):
        """Initialize the display of the players' report"""
        pass

    def get_all_players(self):
        """Displays the player list report in alphabetical order."""
        players_table = Player.dbplayer.table("Players")
        all_players = []
        for player in players_table:
            player_name = player["player_name"]
            all_players.append(player_name)
        sorted_all_players = sorted(all_players)
        print(sorted_all_players)

    def run(self):
        """Method to display the player list report"""
        self.get_all_players()
        return MainMenuController()


class TournamentReportController:
    """Displays the tournament list report."""

    def __init__(self):
        """Initialize the display of the tournaments' report"""
        pass

    def get_all_tournaments(self):
        """Displays the tournament list report in alphabetical order."""
        tournament_table = Tournament.dbtournament.table("Tournaments")
        all_tournaments = []
        for tournament in tournament_table:
            tournament_name = tournament["tournament_name"]
            all_tournaments.append(tournament_name)
        sorted_all_tournaments = sorted(all_tournaments)
        print(sorted_all_tournaments)

    def run(self):
        """Method to display the tournament list report"""
        self.get_all_tournaments()
        return MainMenuController()


class TournamentDateReportController:
    """Displays dates for a given tournament."""

    def __init__(self):
        """Initialize the display of the dates of a tournament."""
        self.get_tournament_name_view = GetTournamentView()
        pass

    def get_tournament_date(self):
        """Displays dates for a given tournament."""
        tournament_name = self.get_tournament_name_view.input_to_get_tournament()
        tournament_table = Tournament.dbtournament.table("Tournaments")
        Tournaments = Query()
        tournament_searched = tournament_table.search(
            Tournaments.tournament_name == tournament_name
        )
        print(tournament_name)
        tournament_start = tournament_searched[0]["tournament_start"]
        print(tournament_start)
        tournament_end = tournament_searched[0]["tournament_end"]
        print(tournament_end)

    def run(self):
        """Method  to display dates for a given tournament."""
        self.get_tournament_date()
        return MainMenuController()


class TournamentPlayerReportController:
    """Displays the list of players registered in a tournament."""

    def __init__(self):
        """Initialize the display of the players's list registered in a tournament"""
        self.get_tournament = AddPlayerTournamentController()

    def get_tournament_players(self):
        """Displays the list of players registered in a tournament."""
        tournament_id = self.get_tournament.get_tournament()
        tournament_players_id_table = (
            AddPlayerTournamentController.dbplayer_tournament.table(
                "Tournaments_Players"
            )
        )
        Players = Query()
        players_searched = tournament_players_id_table.search(
            Players.tournament_id == tournament_id
        )
        players_id = []
        for player in players_searched:
            player_id = player["player_id"]
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
        """Method to display the list of players registered in a tournament."""
        self.get_tournament_players()
        return MainMenuController()


class RoundMatchReportController:
    """Displays the list of rounds of a tournament and the matches of each round."""

    def __init__(self):
        """Initialize the display"""
        self.get_tournament = AddPlayerTournamentController()

    def get_rounds_matches(self):
        """Displays the list of rounds of a tournament and the matches of each round."""
        tournament_id = self.get_tournament.get_tournament()
        rounds_table = Round.dbround.table("Rounds")
        Rounds = Query()
        rounds_searched = rounds_table.search(Rounds.tournament_id == tournament_id)
        rounds_list = []
        for round in rounds_searched:
            round_number = round["round_number"]
            rounds_list.append(round_number)
        print(rounds_list)
        matches_list = []
        for round_number in rounds_list:
            Rounds = Query()
            round_searched = rounds_table.get(
                (Rounds.tournament_id == tournament_id)
                & (Rounds.round_number == round_number)
            )
            round_id = round_searched.doc_id
            matches_table = Match.dbmatch.table("Matches")
            Matches = Query()
            matches_searched = matches_table.search(Matches.round_id == round_id)
            matches_list.append(matches_searched)
        print(matches_list)

    def run(self):
        """Method to display the list of rounds of a tournament and the matches of each round."""
        self.get_rounds_matches()
        return MainMenuController()


class ExitController:
    """Exit the application."""

    def run(self):
        """Method to exit the application."""
        return None
