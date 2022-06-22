pip install .
flask init-db
gunicorn 'wishl:create_app()'