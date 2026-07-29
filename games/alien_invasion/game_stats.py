# author: daniel
# date: 20260618
# location: shanghai
# create the class for the game statistics
from pathlib import Path
import json

class GameStats:
    """follow up the statistics information when playing the game"""
    def __init__(self, ai_game):
        """initialize the statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0

        self.path = Path("highest_score.json")
        if self.path.exists():
            contents = self.path.read_text()
            highest_score = json.loads(contents)
            try:
                self.high_score = int(highest_score)
            except ValueError:
                pass

    def reset_stats(self):
        """initialize the statistics data which could be updated when playing the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_stats(self):
        """save the statistics data, eg saving the highest score"""
        contents = json.dumps(self.high_score)
        self.path.write_text(contents)