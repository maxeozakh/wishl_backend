pipenv shell
pipenv install 
flask init-db
gunicorn 'wishl:create_app()'