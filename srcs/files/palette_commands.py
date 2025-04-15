from textual.command import Hit, Hits, Provider, DiscoveryHit
from textual.app import App, SystemCommand
from textual.screen import Screen
from typing import Iterable, Callable
from functools import partial


class PaletteCommands(Provider):
    """A simple command provider example."""    

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        
        # Define the commands with app reference
        commands = {
            "hello": [self.app.action_say_hello, "Say Hi to a user"],
            "exit": [self.app.action_exit, "Exit the application"],
            "theme": [self.app.action_toggle_theme, "Switch between themes"],
            "help": [self.app.action_help, "Toggle help panel"]
        }

        # Process all commands and assign scores
        hits = []
        for command in commands:
            # Get the match score (even if it's 0)
            score = matcher.match(command)
            # Use a minimum score of 0.1 to ensure all commands appear
            adjusted_score = max(0.1, score)
            
            # Create a Hit object for each command
            # If score was 0, use plain text, otherwise use highlighted text
            display_text = matcher.highlight(command) if score > 0 else command
            
            hits.append(
                Hit(
                    adjusted_score if query else 1.0,  # Use 1.0 for empty queries to show all equally
                    display_text,
                    commands[command][0],
                    help=commands[command][1]
                )
            )
        
        # Sort hits by score (highest first) before yielding
        hits.sort(key=lambda hit: hit.score, reverse=True)
        
        # Yield all hits
        for hit in hits:
            yield hit
    