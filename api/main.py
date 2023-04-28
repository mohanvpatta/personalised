from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils import recommend
from utils import tmdb_id
from utils import custom_thumbnails
from utils import best_rated_movies

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {
        "message": "When you gotta go out and make a movie to pay for the kid's private school and for the three ex-wives, don't talk to me about your artistry. It's their job. It's not my job. It's my calling. ― Quentin Tarantino"
    }


@app.get("/recommend/{user_id}")
async def get_recommend(user_id: int):
    return recommend(user_id)


@app.get("/tmdb/{movie_id}")
async def get_tmdb_id(movie_id: int):
    return tmdb_id(movie_id)


@app.get("/custom/{movie_id}")
async def get_custom_thumnails(movie_id: int):
    return custom_thumbnails(movie_id)


@app.get("/best/{user_id}")
async def get_best_rated_movies(user_id: int):
    return best_rated_movies(user_id)
