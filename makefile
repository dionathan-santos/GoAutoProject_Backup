SHELL := /bin/bash  # Ensure Makefile uses Bash

# Define virtual environment activation
VENV=. .venv/bin/activate  # Use dot (.) instead of source

# Create virtual environment
setup:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

# Install dependencies
install:
	$(VENV) && pip install -r requirements.txt

# Run basic app
run-basic:
	$(VENV) && streamlit run src/app.py

# Run advanced app
run-advanced:
	$(VENV) && streamlit run src/advanced_app.py

# Run tests inside virtual environment
test:
	$(VENV) && PYTHONPATH=$(pwd) pytest test/


# MLFlow-init
mlflow-init:
   @echo " Initializing ML flow server"
   $(PYTHON) src/utils/mlflow_initialize.py

train:
   @echo "Running train.py"
   $(PYTHON) model/train.py

#Run test
predict:
   @echo "Running tests.."
    $(VENV) && python3 predict_api.py

# Clean up temporary files
clean:
	rm -rf __pycache__ */__pycache__		
