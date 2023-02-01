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