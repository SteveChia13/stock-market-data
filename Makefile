# Use variables for readability
PYTHON=python3
VENV=.venv/stock-market-project-venv

# Create virtual environment
dev:
	@echo "Setting up development environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r requirements.txt
	@echo "✅ Environment ready! Activate it with 'source $(VENV)/bin/activate'"

# activate the virtual environment
activate:
	@echo "Activating virtual environment..."
	@source $(VENV)/bin/activate

# Run tests
test:
	@echo "Running tests..."
	@$(VENV)/bin/pytest -v

# Format code (optional)
format:
	@$(VENV)/bin/black .

# Clean cache and temp files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache