from rich.console import Console
from rich.table import Table

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.console = Console()

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        players_by_nationality = [p for p in players if p.nationality == nationality]
        players_by_nationality.sort(key=lambda x: x.points, reverse=True)
        return players_by_nationality

    def show_stats(self, nationality):
        players = self.top_scorers_by_nationality(nationality)

        if not players:
            self.console.print(f"[red]No players found for nationality {nationality}[/red]")
            return

        table = Table(title=f"NHL Players from {nationality}")

        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Team", style="green")
        table.add_column("Goals", justify="right", style="magenta")
        table.add_column("Assists", justify="right", style="magenta")
        table.add_column("Points", justify="right", style="yellow bold")

        for player in players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.points)
            )

        self.console.print(table)
