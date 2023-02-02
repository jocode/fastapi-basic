# FastAPI :ray:

## What is FastAPI?

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

The key features are:
- Fast
- Less errors
- Intuitive
- Easy to learn
- Standard based
- Robust

Libraries used:
- Starlette: Fast ASGI framework/toolkit, on top of which FastAPI is built. Async framework for building APIs.
- Pydantic: Data validation and settings management using Python type hinting.
- Swagger UI: Automatic interactive API documentation.


Who created it?
- Sebastián Ramírez / [@tiangolo](https://twitter.com/tiangolo) (me): Creator of the Starlette and FastAPI projects.


## Instalation of FastAPI and creating your first app

- Create a virtual environment and activate it.
    - `python3 -m venv venv`
    - `source venv/bin/activate`   Linux and Mac
    - `venv\Scripts\activate`      Windows

- Install FastAPI.
    - `pip install fastapi`
    - `pip install uvicorn`

- Addind requirements.txt
    - `pip freeze > requirements.txt`

- Create a file called `main.py` to write your first app.

- To run your app, use the following command:
    - `uvicorn main:app --reload`

- To assign a port to your app, use the following command:
    - `uvicorn main:app --reload --port 5000`

- To run the app in the local network you can use the following command:
    - `uvicorn main:app --reload --port 5000 --host 0.0.0.0`


## Automatic documentation with Swagger UI

FastAPI automatically generates an interactive API documentation (provided by Swagger UI) for your API.

To access to the documentation, go to the URL: `http://your-app-url/docs`
For example:
    - http://localhost:8000/docs

To update the text in the documentation, you can provide the parameters like **title**, **version** and **description** in the `FastAPI()` function.

And for each endpoint, you can add **tags** for the enpoints such a list a description in the `summary` parameter of the `@app.get()` function.

```python
app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
app.description = "Esta es una aplicación de ejemplo para aprender a usar FastAPI"
```

## HTTP methods

The protocol HTTP defines a set of methods to indicate the desired action to be performed for a given resource. Although they can also be nouns, these request methods are sometimes referred to as HTTP verbs. 

The main HTTP methods are:
- GET: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
- POST: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
- PUT: The PUT method replaces all current representations of the target resource with the request payload.
- DELETE: The DELETE method deletes the specified resource.

All the methods are defined in the `@app.get()`, `@app.post()`, `@app.put()` and `@app.delete()` functions.
With that we have the basic structure of a FastAPI app, to build a CRUD using REST API.

### Get Method

GET is used to retrieve data from a server. The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.

```python
@app.get("/movies/")
async def get_movies():
    return movie_list
```

#### Route Parameters

Route parameters are defined in the path of the endpoint. For example, in the following endpoint, the route parameter is `movie_id`:


```python
@app.get('/movies/{movie_id}', tags=['movies'])
def get_movie(movie_id: int):
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    return []
```

#### Query Parameters

Query parameters are defined in the URL of the endpoint. Is defined as a key-value pair in the URL. For example, in the following endpoint, the query parameter is `movie_id`:

```python
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: str = None):
    movies = [movie for movie in movie_list if movie['category'] == category]

    if year:
        movies = [movie for movie in movies if movie['year'] == year]

    return movies
```

### Post Method

POST is used to send data to a server to create/update a resource. The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.

```python
@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    movie = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    movie_list.append(movie)
    return movie
```

### Put Method

PUT is used to send data to a server to create/update a resource. The PUT method replaces all current representations of the target resource with the request payload.

```python
@app.put('/movies/{movie_id}', tags=['movies'])
def update_movie(movie_id: int, title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    for movie in movie_list:
        if movie['id'] == movie_id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
            return movie
    return []
```

## Schemas

Pydantic is a data validation and settings management library using Python type hinting. It is used to define the data models for the API.

```python
from pydantic import BaseModel

class Movie(BaseModel):
    id: Optional[int]
    title: str
    overview: str
    year: int
    rating: float
    category: str

# We could use the Movie class to define the body of the request
@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movie_list.append(movie.dict())
    return movie

@app.put('/movies/{movie_id}', tags=['movies'])
def update_movie(movie_id: int, movie: Movie):
    for item in movie_list:
        if item['id'] == movie_id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return item
    return []
```


## Data Type Validation

FastAPI provides a set of data types to validate the data in the request body, path parameters, query parameters, etc.

We can add other validations to the data types. For example, we can add a minimum and maximum value to the `int` data type using the **`Field`** class from Pydantic.

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int]
    title: str : Field(min_lenght=5, max_length=100)
    overview: str
    year: int = Field(gt=1900, lt=2023)
    rating: float
    category: str
```

For numeric values, we can use the **`gt`** and **`lt`** parameters to define the minimum and maximum value. For strings, we can use the **`min_lenght`** and **`max_length`** parameters to define the minimum and maximum length.

- **gt**: greater than
- **ge**: greater than or equal
- **lt**: less than
- **le**: less than or equal

:book: [Path params numeric validations](https://fastapi.tiangolo.com/es/tutorial/path-params-numeric-validations/#recap)

Also, we can use the **`regex`** parameter to define a regular expression to validate the data.

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int]
    title: str : Field(min_lenght=5, max_length=100)
    overview: str
    year: int = Field(gt=1900, lt=2023)
    rating: float
    category: str = Field(regex='^(action|comedy|drama|horror|romance)$')
```

For define a default scheme, we can use the **`BaseModel`** class from Pydantic and add a new class inside call **`Config`**.

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=5, max_length=100, default="No title")
    overview: str = Field(min_length=10, max_length=500, default="No overview")
    year: int = Field(gt=1900, lt=2023)
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Avatar",
                "overview": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
                "year": 2009,
                "rating": 7.8,
                "category": "Action"
            }
        }
```

## Params Validation

We can use the **`Path`** and **`Query`** classes from FastAPI to validate the data in the path parameters and query parameters.

```python
from fastapi import FastAPI, Path, Query

@app.get('/movies/{movie_id}', tags=['movies'])
def get_movie(movie_id: int = Path(..., title="The ID of the movie to get", ge=1, le=1000)):
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15), year: str = None):
    movies = []
    for movie in movie_list:
        if movie['category'] == category:
            movies.append(movie)

    if year:
        movies = [movie for movie in movies if movie['year'] == year]
    return movies
```


By default, FastAPI converts the returned values to JSON, transforming and using JSONResponse behind the scenes. It would not be entirely necessary to use JSONResponse if it is not for a specific case.

:book: [Response directly](https://fastapi.tiangolo.com/advanced/response-directly/)


## Response Type

To specify the response type, we can use the **`response_model`** parameter in the function decorator.
And for list of objects, we can use the **`List`** class from **typing** module.

```python
from fastapi import FastAPI, Path, Query
from typing import Optional, List

@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
def get_movie(movie_id: int = Path(..., title="The ID of the movie to get", ge=1, le=1000)):
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    return []

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies():
    return movie_list
```

Or alternatively, we can specify the response type in the function definition, like that **` -> Movie`**

```python
from fastapi import FastAPI, Path, Query
from typing import Optional, List

@app.get('/movies/{movie_id}', tags=['movies'])
def get_movie(movie_id: int = Path(title="The ID of the movie to get", ge=1, le=1000)) -> Movie:
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    return []
```

## Status Code

To specify the status code, we can use the **`status_code`** parameter in the function decorator. And import the **`status`** module from FastAPI.

:book: [Status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

```python
from fastapi import FastAPI, Path, Query, status

@app.post('/movies', tags=['movies'], status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):
    movie_list.append(movie.dict())
    return movie
```

To define HTTP status codes, we can use the **`HTTPException`** class from FastAPI.

```python
from fastapi import FastAPI, Path, Query, status, HTTPException

@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
def get_movie(movie_id: int = Path(..., title="The ID of the movie to get", ge=1, le=1000)):
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {movie_id} not found")
```