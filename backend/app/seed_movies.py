import requests
import time

TMDB_API_KEY = "API_KEY"
FASTAPI_URL = "http://127.0.0.1:8000/movies/"
WINDOW_SIZE = 5

GENRE_MAPPING = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
    99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance", 878: "Sci-Fi",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

def populate_db():
    print("Starting to populate the database with popular movies from TMDB...")
    movies_added = 0
    
    for page in range(1, WINDOW_SIZE + 1):
        tmdb_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
        
        try:
            response = requests.get(tmdb_url)
            if response.status_code != 200:
                print(f"Failed to fetch data from TMDB for page {page}. Status code: {response.status_code}")
                continue
            
            movie_data = response.json().get("results", [])
            
            for movie in movie_data:
                title = movie.get("title")
                description = movie.get("overview", "")
                genre_ids = movie.get("genre_ids", [])
                
                genre_name = GENRE_MAPPING.get(genre_ids[0], "Unknown") if genre_ids else "Unknown"
                
                payload = {
                    "title": title,
                    "genre": genre_name,
                    "description": description
                }
                
                fastapi_response = requests.post(FASTAPI_URL, json=payload)
                
                if fastapi_response.status_code == 200:
                    print(f"Successfully added movie: {title} ({genre_name})")
                    movies_added += 1
                else:
                    print(f"Failed to add movie: {title}. Status code: {fastapi_response.status_code}")
                time.sleep(0.5)
                
        except Exception as e:
            print(f"An error occurred while processing page {page}: {e}")
        
    print(f"Finished populating the database. Total movies added: {movies_added}")

if __name__ == "__main__":
    populate_db()