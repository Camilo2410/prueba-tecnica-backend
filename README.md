## Setup (Ubuntu/Pop!_OS)

### 1) System dependencies (required for mysqlclient)
sudo apt update
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

### 2) Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

### 3) Install Python dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

### 4) Configure environment variables
cp .env.example .env

### 5) Run migrations and server
python manage.py migrate
python manage.py runserver