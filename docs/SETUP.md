# Create virtual environment
python3 -m venv .venv

# Activate (Linux / macOS)
source .venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run Docker
docker compose up --build

