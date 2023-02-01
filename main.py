from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
app.description = "FastAPI documentation"

# Movies list
movie_list = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
        "year": "2009",
        "rating": 7.8,
        "category": "Action"
    }
]


@app.get("/", tags=["home"], description="Hola")
def message():
    return {
        "hello": "world"
    }


@app.get('/html', tags=["home"])
def return_html():
    return HTMLResponse(
        '''
        <h1>Hello world</h1>
        '''
    )


@app.get('/movies', tags=['movies'])
def get_movies():
    return movie_list


@app.get('/movies/{movie_id}', tags=['movies'])
def get_movie(movie_id: int):
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    return []


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: str = None):
    movies = []
    for movie in movie_list:
        if movie['category'] == category:
            movies.append(movie)

    if year:
        movies = [movie for movie in movies if movie['year'] == year]
    return movies


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


@app.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(movie_id: int):
    for movie in movie_list:
        if movie['id'] == movie_id:
            movie_list.remove(movie)
            return movie
    return []