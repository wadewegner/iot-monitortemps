virtualenv venv
source venv/bin/activate

pip install Flask gunicorn
created file: /src/web/main.py

created Profile
	web: gunicorn --pythonpath=./src/web main:app


pip freeze > requirements.txt