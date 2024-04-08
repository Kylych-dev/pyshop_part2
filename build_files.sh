# Build the project
# echo "Building the project..."
python3.9 -m venv env
source env/bin/activate
pip3 install --upgrade pip
pip3 install django djangorestframework
pip3 install -r requirements.txt

# echo "Make Migration..."
find . -path "*/migrations/*.py" -not -path "*/site-packages/*" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
python3.9 manage.py makemigrations accounts
python3.9 manage.py migrate --run-syncdb --noinput
python3.9 manage.py makemigrations --noinput

# echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear