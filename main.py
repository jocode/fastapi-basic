from fastapi import FastAPI, Body, Path, Query, status, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
app.description = "FastAPI documentation"


class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=5, max_length=100, default="No title")
    overview: str = Field(min_length=10, max_length=500, default="No overview")
    year: int = Field(gt=1900, lt=2023)
    rating: float = Field(gt=0, lt=10)
    category: str = Field(min_length=3, max_length=20, default="No category")

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



# Movies list
movie_list = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.",
        "year": 2009,
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


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies():
    return movie_list


@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie(movie_id: int = Path(title="The ID of the movie to get", ge=1, le=1000)):
    for movie in movie_list:
        if movie['id'] == movie_id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {movie_id} not found")


@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15), year: str = None):
    movies = []
    for movie in movie_list:
        if movie['category'] == category:
            movies.append(movie)

    if year:
        movies = [movie for movie in movies if movie['year'] == year]
    return movies


@app.post('/movies', tags=['movies'], response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> Movie:
    movie_list.append(movie.dict())
    return movie


@app.put('/movies/{movie_id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def update_movie(movie_id: int, movie: Movie) -> Movie:
    for item in movie_list:
        if item['id'] == movie_id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")


@app.delete('/movies/{movie_id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def delete_movie(movie_id: int) -> Movie:
    for movie in movie_list:
        if movie['id'] == movie_id:
            movie_list.remove(movie)
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")