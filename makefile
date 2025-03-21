# Makefile for GoAuto Project

# Detect the operating system
ifeq ($(OS),Windows_NT)
    PYTHON = python
    VENV_ACTIVATE = venv\Scripts\activate
    RM = rmdir /s /q
    MKDIR = mkdir
else
    PYTHON = python3
    VENV_ACTIVATE = venv/bin/activate
    RM = rm -rf
    MKDIR = mkdir -p
endif

# Phony targets
.PHONY: help setup clean test run lint format deps update-deps mlflow-clean mlflow-reset

# Help target
help:
	@echo "Available targets:"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  clean       - Remove virtual environment and temporary files"
	@echo "  test        - Run project tests"
	@echo "  run         - Run the main application"
	@echo "  lint        - Run code linters"
	@echo "  format      - Format code using black"
	@echo "  deps        - Install project dependencies"
	@echo "  update-deps - Update project dependencies"
	@echo "  mlflow-clean - Clean MLflow artifacts"
	@echo "  mlflow-reset - Reset MLflow configuration"

# Setup virtual environment and install dependencies
setup: clean
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv venv
	. $(VENV_ACTIVATE) && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

# Clean up temporary files and virtual environment
clean:
	@echo "Cleaning up project..."
	$(RM) venv
	$(RM) .pytest_cache
	$(RM) .coverage
	find . -type d -name "__pycache__" -exec $(RM) {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete

# Run project tests
test:
	@echo "Running project tests..."
	. $(VENV_ACTIVATE) && \
	pytest test/

# Run the main application
run:
	@echo "Running the application..."
	. $(VENV_ACTIVATE) && \
	streamlit run src/app.py

# Run code linters
lint:
	@echo "Running code linters..."
	. $(VENV_ACTIVATE) && \
	flake8 src/ test/

# Format code using black
format:
	@echo "Formatting code..."
	. $(VENV_ACTIVATE) && \
	black src/ test/

# Install project dependencies
deps:
	@echo "Installing project dependencies..."
	. $(VENV_ACTIVATE) && \
	pip install -r requirements.txt

# Update project dependencies
update-deps:
	@echo "Updating project dependencies..."
	. $(VENV_ACTIVATE) && \
	pip list --outdated
	@echo "Please manually update versions in requirements.txt"

# Clean MLflow artifacts
mlflow-clean:
	@echo "Cleaning MLflow artifacts..."
	$(RM) mlruns/
	$(RM) mlartifacts/
	$(RM) mlflow.db
	$(RM) mlruns.db

# Reset MLflow configuration
mlflow-reset: mlflow-clean
	@echo "Resetting MLflow configuration..."
	$(MKDIR) mlflow_config
	cp mlflow_config/config.yaml mlflow_config/config.yaml.bak 2>/dev/null || true

# Create a requirements file from current environment
freeze:
	@echo "Freezing current environment dependencies..."
	. $(VENV_ACTIVATE) && \
	pip freeze > requirements-frozen.txt