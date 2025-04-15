CSS = """

Header {
    height: 1;
}

Footer {
    height: 1;
}

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
    margin-bottom: 1;
    width: 100%;
    color: $success;
    text-style: bold;
}

.error {
    color: $error;
}

/* Option list styling */
#option-list {
    width: 60%;
    height: auto;
    margin: 1;
    border: heavy $accent;
    background: $surface;
    display: none;  /* Hidden by default */
}

#option-list:focus {
    border: heavy $accent-lighten-2;
}

/* Enhanced command input styling */
#command-input {
    dock: bottom;
    width: 100%;
    height: 3;  /* Increased height */
    border: $accent;  /* Added border */
    background: $surface-darken-1;  /* Slightly different background */
    padding: 0 1;
    margin: 1 0;  /* Added margin for spacing */
}

#command-input:focus {
    border: $accent-lighten-2;  /* Highlight border when focused */
}

#command-input > .input--cursor {
    background: $accent;  /* Custom cursor color */
    color: $text;
}

/* Make the placeholder text more visible */
#command-input > .input--placeholder {
    color: $text-muted;
    opacity: 0.7;
}

/* Help panel styles */
#help-panel {
    dock: right;
    width: 30;
    height: 100%;
    background: $panel;
    padding: 1;
    border-left: solid $accent;
}

.help-title {
    color: $accent;
    text-align: center;
    text-style: bold;
    margin-bottom: 1;
}

.help-command {
    margin-bottom: 1;
    padding-left: 1;
}

/* Command palette styles */
CommandPalette {
    width: 60%;
    margin: 1;
    border: heavy $accent;
}

"""