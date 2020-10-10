export FLASK_APP=app
export FLASK_ENV=development
export POSTGRES_USERNAME=lam
export POSTGRES_PASSWORD=lam585

sh ./postgres_env.sh
flask run