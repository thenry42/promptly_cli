CSS = """
/* Base layout */
Header {
    height: 1;
}

/* Terminal output area */
#terminal-output {
    width: 100%;
    height: 1fr;
    background: $surface;
    padding: 1;
    border: solid $primary;
}

.output-line {
    margin-bottom: 1;
    width: 100%;
}

.command-line {
    width: 100%;
    color: $success;
    text-style: bold;
}

.error {
    color: $error;
}

/* Prompt container styling */
.prompt-container {
    width: 100%;
    height: auto;
    margin-top: 0;
    margin-bottom: 0;
}

.prompt {
    color: $success;
    text-style: bold;
    width: auto;
    min-width: 2;
}

/* Make the input field blend with the terminal */
#command-input {
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    width: 1fr;
    height: 1;
}

#command-input:focus {
    border: none;
}

#command-input > .input--cursor {
    background: $accent;
    color: $text;
}

/* Option list */
#option-list {
    width: 60%;
    height: auto;
    margin: 1;
    border: heavy $accent;
    background: $surface;
    display: none;
}

#option-list:focus {
    border: heavy $accent-lighten-2;
}
"""