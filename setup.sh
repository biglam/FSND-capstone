export FLASK_APP=app
export FLASK_ENV=development
export DATABASE_URL="postgres://lam:lam585@localhost:5432/capstone"

sh ./postgres_env.sh
flask run