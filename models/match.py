from models.player import Player

"""Docstring."""

class Match:
    """Match"""
    def __init__(self, player_A: Player, player_B: Player, score_A='', score_B=''):
        self.match_saved = ([player_A, score_A], [player_B, score_B])

