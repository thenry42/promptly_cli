def handle_command(user_input):
    """
    Handle the command from the user.
    Switch case for the command.
    Return False if the program should exit.
    Return True when the command is handled.
    """

    cmd = user_input.split(" ")
    
    if cmd[0] in ("exit", "quit"):
        return False
    else:
        print(user_input)
        return True