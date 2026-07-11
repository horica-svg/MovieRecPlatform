from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from ml_model import recommend_movies
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personalized Movie Recommendation System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/movies/", response_model=schemas.MovieResponse)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(title=movie.title, genre=movie.genre, description=movie.description)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=List[schemas.MovieResponse])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    return movies

@app.get("/movies/{movie_id}/recommendations", response_model=List[schemas.MovieResponse])
def get_recommendations(movie_id: int, top_n: int = 3, db: Session = Depends(get_db)):
    movie_base = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie_base:
        raise HTTPException(status_code=404, detail="Movie not found")
    recommended_movies = recommend_movies(movie_id=movie_id, db=db, top_n=top_n)
    return recommended_movies