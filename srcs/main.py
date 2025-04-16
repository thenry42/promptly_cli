import sys

def main():
    args = sys.argv[1:]  # Get all command line arguments except the script name
    
    if not args:
        # No arguments were provided
        print("Hello, world!")
    else:
        # Print each argument on a new line
        for i, arg in enumerate(args, 1):
            print(f"Argument {i}: {arg}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()