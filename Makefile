# Simple Makefile for Python project

.PHONY: setup test clean run exe

# Configuration
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SRCS = srcs

# Create and set up virtual environment
setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(SRCS)/requirements.txt
	@echo "Development environment set up successfully"

# Run the application
run:
	@$(PYTHON) $(SRCS)/main.py

# Run with arguments
runwith:
	@$(PYTHON) $(SRCS)/main.py $(ARGS)

# Run tests (when you add them)
test:
	$(VENV)/bin/pytest $(SRCS)

# Create standalone executable
exe: setup
	$(PIP) install pyinstaller
	$(VENV)/bin/pyinstaller --onefile --name promptly $(SRCS)/main.py
	@echo "Executable created at dist/promptly"

# Clean project files
clean:
	rm -rf build/ dist/ *.egg-info/ $(VENV) *.spec
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Display help information
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup      Create virtual environment and install dependencies"
	@echo "  run        Run the application"
	@echo "  runwith    Run with arguments (make runwith ARGS=\"arg1 arg2\")"
	@echo "  test       Run the test suite"
	@echo "  exe        Create standalone executable"
	@echo "  clean      Remove temporary files and build artifacts"
