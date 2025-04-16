import sys
from files.man import Usage, list, run, help
from files.config import load_environment, debug_env_vars

def main():
    # Force reload environment variables on each run
    load_environment(force_reload=True)
    
    # Uncomment for debugging
    # debug_env_vars()
    
    args = sys.argv[1:]  # Get all command line arguments except the script name
    
    if not args:
        # No arguments were provided
        Usage()
    else:
        # Process command line arguments
        if args[0] == "list":
            list(args)
        elif args[0] == "run":
            run(args)
        elif args[0] == "help":
            help()
        elif args[0] == "debug":
            # Add a debug command to show environment variables
            debug_env_vars()

    sys.exit(0)

if __name__ == "__main__":
    main()