import signal
import os
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
import re
from files.llm_global import chat_completion

def chat(provider, model):
    console = Console()
    
    # Set up prompt_toolkit session with history
    history_file = os.path.join(os.path.expanduser("~"), ".promptly_history")
    
    # Initialize an empty completer - we'll update it with history words
    chat_completer = WordCompleter([], ignore_case=True)
    
    # Try to pre-populate the completer from existing history
    history_words = set()
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Extract words from history
                    words = re.findall(r'\b\w+\b', line)
                    for word in words:
                        if len(word) > 3:  # Only add substantial words
                            history_words.add(word)
            
            # Update the completer with initial words from history
            chat_completer = WordCompleter(list(history_words), ignore_case=True)
    except Exception:
        # If there's any issue, just continue with an empty completer
        pass
    
    session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=chat_completer,
        enable_history_search=True,
        complete_in_thread=True,
        complete_while_typing=True
    )
    
    # Define prompt style
    prompt_style = Style.from_dict({
        'prompt': 'bold blue',
    })
    
    console.print("[bold green]Welcome to the AI Chat![/bold green] Type your message and press Enter. Press Ctrl+D to exit.")
    console.print("[bold yellow]Tip: Use arrow keys to navigate history, Tab for suggestions, Ctrl+C for a new prompt.[/bold yellow]")
    console.print()

    # Keep track of words to add to the completer
    all_words = history_words.copy()
    
    # Initialize conversation history for the LLM
    messages = []

    while True:
        try:
            # Use prompt_toolkit for input with proper history and arrow key support
            user_input = session.prompt(
                "You: ", 
                style=prompt_style,
                enable_system_prompt=True,
                enable_suspend=True  # Allow Ctrl+Z to suspend
            )
            
            if user_input.strip() == "":
                continue

            # Extract words from the current input to add to the completer
            new_words = re.findall(r'\b\w+\b', user_input)
            for word in new_words:
                if len(word) > 3 and word not in all_words:  # Only add substantial words
                    all_words.add(word)
            
            # Update the completer with new words
            session.completer = WordCompleter(list(all_words), ignore_case=True)

            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Get AI response using chat_completion
            ai_response = chat_completion(provider, model, user_input, messages)
            
            # Add AI response to conversation history if we got a valid response
            if ai_response:
                messages.append({"role": "assistant", "content": ai_response})
                
                # Extract words from AI response to add to the completer as well
                ai_words = re.findall(r'\b\w+\b', ai_response)
                for word in ai_words:
                    if len(word) > 3 and word not in all_words:  # Only add substantial words
                        all_words.add(word)
                
                # Update the completer again with AI response words
                session.completer = WordCompleter(list(all_words), ignore_case=True)

        except EOFError:
            # Handle Ctrl+D
            console.print("\n[bold red]Goodbye![/bold red]")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C - display new prompt
            console.print("\n[bold yellow]Starting a new prompt...[/bold yellow]")
            continue

    return 0