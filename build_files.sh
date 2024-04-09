python3.9 -m venv env
source env/bin/activate
# pip3 install --upgrade pip
/vercel/path0/env/bin/python3.9 -m pip install --upgrade pip
print('pwd', '=================================================')
pip3 install django djangorestframework
pip3 install -r requirements.txt 
python3.9 manage.py collectstatic --noinput --clear


# # Build the project
# # echo "Building the project..."
# python3.9 -m venv env
# source env/bin/activate

# # pip3 install --upgrade pip
# # pip3 install django djangorestframework
# # pip3 install -r requirements.txt

# pip install --upgrade pip
# pip install django djangorestframework
# pip install -r requirements.txt

# # echo "Make Migration..."
# find . -path "*/migrations/*.py" -not -path "*/site-packages/*" -delete
# find . -type d -name "__pycache__" -exec rm -rf {} +
# python3.9 manage.py makemigrations accounts
# python3.9 manage.py migrate --run-syncdb --noinput
# python3.9 manage.py makemigrations --noinput

# # echo "Collect Static..."
# python3.9 manage.py collectstatic --noinput --clear





# Создание виртуального окружения и активация
# sudo apt update
# sudo apt install python3.9

# python3.9 -m venv env
# source env/bin/activate

# # Обновление pip и установка зависимостей
# pip install --upgrade pip
# pip install django djangorestframework
# pip install -r requirements.txt

# # Удаление старых миграций и очистка __pycache__
# find . -path "*/migrations/*.py" -not -path "*/site-packages/*" -delete
# find . -type d -name "__pycache__" -exec rm -rf {} +

# # Выполнение миграций и сборка статических файлов
# python3 manage.py makemigrations
# python3 manage.py migrate --run-syncdb --noinput
# python3 manage.py makemigrations --noinput
# python3 manage.py collectstatic --noinput --clear




# # Активация виртуального окружения
# source env/bin/activate

# # Обновление pip и установка зависимостей
# pip install --upgrade pip
# pip install -r requirements.txt

# # Удаление старых миграций и очистка __pycache__
# # find . -path "*/migrations/*.py" -not -path "*/site-packages/*" -delete
# # find . -type d -name "__pycache__" -exec rm -rf {} +

# # Выполнение миграций и сборка статических файлов
# python manage.py makemigrations
# python manage.py migrate
# python manage.py collectstatic
