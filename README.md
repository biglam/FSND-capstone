# FSND-capstone

## Getting started

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Running the server 
```bash
export POSTGRES_USERNAME=*postgres username*
export POSTGRES_PASSWORD=*postgres password*
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
---
## Endpoints

```
GET    '/movies' - lists all movies
GET    '/movies/{movie id}' - lists a single movies data by id
POST   '/movies/' - creates a new movie from a JSON form
PATCH  '/movies/{movie id}' - updates a movies existing data
DELETE '/movies/{movie id}' - deletes a movies record from the database
GET    '/actors' - lists all actors
GET    '/actors/{actor id}' - lists a single actors data by id
POST   '/actors/' - creates a new actor from a JSON form
PATCH  '/actors/{actor id}' - updates a actors existing data
DELETE '/actors/{actor id}' - deletes a actors record from the database
```
