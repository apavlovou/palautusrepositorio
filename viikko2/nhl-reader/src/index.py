from rich.console import Console
from rich.prompt import Prompt
from player_reader import PlayerReader
from player_stats import PlayerStats

def main():
    console = Console()
    console.print("[blue]NHL Statistics[/blue]", style="bold")
    
    while True:
        season = Prompt.ask("Enter season (e.g., 2024-25) or 'quit' to exit")
        
        if season.lower() == 'quit':
            break
            
        nationality = Prompt.ask("Enter nationality (e.g., FIN, SWE, CAN)")
        
        reader = PlayerReader(season)
        stats = PlayerStats(reader)
        stats.show_stats(nationality.upper())

if __name__ == "__main__":
    main()
