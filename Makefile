# Makefile for Python application with virtual environment

.PHONY: setup install run clean test help

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PROJECT_DIR = srcs
REQUIREMENTS = $(PROJECT_DIR)/requirements.txt

help:
	@echo "Available commands:"
	@echo "  make setup    - Create virtual environment"
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Run the application"
	@echo "  make clean    - Remove virtual environment and cache files"
	@echo "  make help     - Show this help message"

$(VENV):
	python -m venv $(VENV)

setup: $(VENV)
	@echo "Virtual environment created at $(VENV)"

install: setup
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	@echo "Dependencies installed successfully"

run: install
	@clear
	@echo "┌───────────────────────────────────────────┐"
	@echo "│             Running SheLLM                │"
	@echo "└───────────────────────────────────────────┘"
	@echo ""
	@cd $(PROJECT_DIR) && ../$(PYTHON) main.py
	@echo ""
	@echo "┌───────────────────────────────────────────┐"
	@echo "│        Program execution complete         │"
	@echo "└───────────────────────────────────────────┘"

clean:
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	@echo "Cleaned up project files"
