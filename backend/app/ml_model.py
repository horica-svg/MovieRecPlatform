import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
import models

def recommend_movies(movie_id: int, db: Session, top_n: int = 3):
    movies = db.query(models.Movie).all()
    
    if not movies or len(movies) < 2:
        return []
    
    data = [{
        "id": m.id,
        "title": m.title,
        "genre": m.genre,
        "description": m.description or "",
    } for m in movies]
    
    df = pd.DataFrame(data)
    
    df["metadata"] = df["genre"] + " " + df["description"]
    
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["metadata"])
    
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    if movie_id not in df["id"].values:
        return []
    
    idx = df[df["id"] == movie_id].index[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:top_n + 1]
    
    movie_indices = [i[0] for i in sim_scores]
    recommended_ids = df["id"].iloc[movie_indices].tolist()
    
    return db.query(models.Movie).filter(models.Movie.id.in_(recommended_ids)).all()