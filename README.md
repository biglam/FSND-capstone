# FSND-capstone

## Getting started

### Installing dependencies
This project requires Python and pip. Once these are available, the dependencies can all be installed by running:
```bash
pip install -r requirements.txt
```

### Running the server 
There is a bash script included to start the server. To use, edit the POSTGRES_USERNAME and POSTGRES_PASSWORD values in ```setup.sh``` and run:
```bash
    sh ./setup.sh
```
Note that this starts the server in development mode.

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
PUT   '/movie/{movie id}/actor/{actor id}' - adds actor to movie
DELETE '/movie/{movie id}/actor/{actor id}' - removes actor from movie
PUT   '/actor/{actor id}/movie/{movie id}' - adds movie to actor
DELETE '/actor/{actor id}/movie/{movie id}' - removes movie from actor
```

**GET '/movies'**
- Fetches a list of all movies
- Request Arguments: None
- Returns: an object with two keys, movies (contains an array of movie data), and success (indicates a successful transaction) 
```JSON
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 01 Feb 2000 00:00:00 GMT",
            "title": "movie 1"
        },
        {
            "id": 2,
            "release_date": "Fri, 01 Feb 2002 00:00:00 GMT",
            "title": "movie 2"
        },
        {
            "id": 3,
            "release_date": "Thu, 21 Feb 1980 00:00:00 GMT",
            "title": "movie 3"
        },
        {
            "id": 4,
            "release_date": "Fri, 25 Dec 2020 00:00:00 GMT",
            "title": "xmas movie"
        }
    ],
    "success": true
}
```
---
**GET '/movies/{movie id}'**
- Fetches all data about a specific movie
- Request Arguments: None
- Returns: an object with two keys, movie (contains movie data), and success (indicates a successful transaction) 
```JSON
{
    "movie": {
        "actors": [
            {
                "id": 2,
                "name": "john"
            },
            {
                "id": 4,
                "name": "anna"
            }
        ],
        "id": 1,
        "release_date": "Tue, 01 Feb 2000 00:00:00 GMT",
        "title": "movie 1"
    },
    "success": true
}
```
---
**POST '/movies'**
- Creates a new movie in the database using the provided data
- Sample Requests: 
    - Required Fields:
        ```JSON
        {
            "title": "xmas movie",
            "release_date": "2020-12-25"
        }
        ```
    - With optional array of actor id's:
         ```JSON
        {
            "title": "xmas movie",
            "release_date": "2020-12-25",
            "actors": [1, 2, 3]
        }
        ```
- Returns: 
    - The ID and data of the newly created movie
```json
{
    "movie": {
        "actors": [],
        "id": 4,
        "release_date": "Fri, 25 Dec 2020 00:00:00 GMT",
        "title": "xmas movie"
    },
    "success": true
}
```
---
**PATCH '/movies/{movie id}'**
- Updates a movie in the database using the provided data
- Request Arguments (json formatted). Only changed fields are required: 
```JSON
{
    "release_date": "2010-02-10"
}
```
- Returns: 
    - The ID and data of the newly updated movie
```json
{
    "movie": {
        "actors": [
            {
                "id": 2,
                "name": "john"
            },
            {
                "id": 4,
                "name": "anna"
            }
        ],
        "id": 1,
        "release_date": "Wed, 10 Feb 2010 00:00:00 GMT",
        "title": "movie 1"
    },
    "success": true
}
```
---
**DELETE '/movies/{movie id}'**
- Deletes a movie and its associated records
- Returns: 
    - The ID of the deleted movie
```json
{
    "deleted_id": 3,
    "success": true
}
```
---
**GET '/actors'**
- Fetches a list of all actors
- Request Arguments: None
- Returns: an object with two keys, actors (contains an array of actor data), and success (indicates a successful transaction) 
```JSON
{
    "actors": [
        {
            "age": 50,
            "gender": "male",
            "id": 1,
            "name": "jim"
        },
        {
            "age": 21,
            "gender": "male",
            "id": 2,
            "name": "john"
        },
        {
            "age": 24,
            "gender": "female",
            "id": 3,
            "name": "jenny"
        },
        {
            "age": 60,
            "gender": "female",
            "id": 4,
            "name": "anna"
        }
    ],
    "success": true
}
```
---
**GET '/actors/{actor id}'**
- Fetches all data about a specific actor
- Request Arguments: None
- Returns: an object with two keys, actor (contains actor data), and success (indicates a successful transaction) 
```JSON
{
    "actor": {
        "age": 50,
        "gender": "male",
        "id": 1,
        "movies": [
            {
                "id": 2,
                "title": "movie 2"
            }
        ],
        "name": "jim"
    },
    "success": true
}
```
---
**POST '/actors'**
- Creates a new actor in the database using the provided data
- Sample Requests (json formatted): 
  - standard
    ```JSON
    {
        "name": "anna",
        "age": 60,
        "gender": "female"
    }
    ```
  - with optional array of movie id's
      ```JSON
    {
        "name": "anna",
        "age": 60,
        "gender": "female",
        "movies": [1, 2, 3]
    }
    ```

- Returns: 
    - The ID and data of the newly created actor
```json
{
    "actor": {
        "age": 60,
        "gender": "female",
        "id": 5,
        "movies": [],
        "name": "anna"
    },
    "success": true
}
```
---
**PATCH '/actors/{actor id}'**
- Updates a actor in the database using the provided data
- Request Arguments (json formatted). Only changed fields are required: 
```JSON
{
    "name": "Irene"
}
```
- Returns: 
    - The ID and data of the newly updated actor
```json
{
    "actor": {
        "age": 60,
        "gender": "female",
        "id": 5,
        "movies": [],
        "name": "Irene"
    },
    "success": true
}
```
---
**DELETE '/actors/{actor id}'**
- Deletes a actor and its associated records
- Returns: 
    - The ID of the deleted actor
```json
{
    "deleted_id": 3,
    "success": true
}
```
---
**PUT '/movies/{movie id}/actors/{actor id}'**
- Appends an actor to the movie 
- Returns: 
    - The ID and data of the updated movie
```json
{
    "movie": {
        "actors": [
            {
                "id": 4,
                "name": "anna"
            }
        ],
        "id": 2,
        "release_date": "Fri, 01 Feb 2002 00:00:00 GMT",
        "title": "movie 2"
    },
    "success": true
}
```
---
**DELETE '/movies/{movie id}/actors/{actor id}'**
- Removes an actor from a movie 
- Returns: 
    - The ID and data of the updated movie
```json
{
    "movie": {
        "actors": [],
        "id": 2,
        "release_date": "Fri, 01 Feb 2002 00:00:00 GMT",
        "title": "movie 2"
    },
    "success": true
}
```
---
**PUT '/actors/{actor id}/movies/{movie id}'**
- Appends an movie to the actor 
- Returns: 
    - The ID and data of the updated actor
```json
{
    "actor": {
        "age": 60,
        "gender": "female",
        "id": 4,
        "movies": [
            {
                "id": 2,
                "title": "movie 2"
            },
            {
                "id": 1,
                "title": "movie 1"
            }
        ],
        "name": "anna"
    },
    "success": true
}
```
---
**DELETE '/actors/{actor id}/movies/{movie id}'**
- Removes an movie from a actor 
- Returns: 
    - The ID and data of the updated actor
```json
{
    "actor": {
        "age": 60,
        "gender": "female",
        "id": 4,
        "movies": [
            {
                "id": 1,
                "title": "movie 1"
            }
        ],
        "name": "anna"
    },
    "success": true
}
```