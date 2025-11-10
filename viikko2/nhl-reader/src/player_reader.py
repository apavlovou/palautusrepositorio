import requests
from player import Player

class PlayerReader:
    def __init__(self, season):
        self.url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"

    def get_players(self):
        try:
            response = requests.get(self.url, timeout=5).json()
            players = []

            for player_dict in response:
                players.append(Player(player_dict))

            return players
        except (requests.RequestException, ValueError) as error:
            print(f"Error fetching players: {error}")
            return []
