#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

touch .envrc &&
echo '
export SECRET_KEY=""
export SECRET_TOKEN=""
export HOST=""
export DB_NAME=""
export DB_PASSWORD=""
export DB_USER=""
' > .envrc

source .envrc

python manage.py makemigrations
python manage.py migrate
