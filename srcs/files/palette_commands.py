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
            "theme": [self.app.action_toggle_theme, "Switch between themes"]
        }

        for command in commands:
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),
                    commands[command][0],
                    help=commands[command][1]
                )
    