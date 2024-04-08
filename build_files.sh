# Build the project
# echo "Building the project..."
python3.9 -m venv env
source env/bin/activate
python3.9 -m pip install --upgrade pip
pip install django djangorestframework
python3.9 -m pip install -r requirements.txt

# echo "Make Migration..."
find . -path "*/migrations/*.py" -not -path "*/site-packages/*" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
python3.9 manage.py migrate --run-syncdb --noinput&& 
python3.9 manage.py makemigrations --noinput && 

# echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear