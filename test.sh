export POSTGRES_PASSWORD=lam585
export POSTGRES_USERNAME=lam

dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.sql

python test_flaskr.py