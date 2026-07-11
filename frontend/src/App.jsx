import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const API_URL = "http://127.0.0.1:8000";

  // Încarcă automat filmele preluate din TMDb la pornirea aplicației
  useEffect(() => {
    fetchMovies();
  }, []);

  const fetchMovies = async () => {
    try {
      const response = await axios.get(`${API_URL}/movies/?limit=106`);
      setMovies(response.data);
    } catch (error) {
      console.error(
        "Error occurred while fetching movies from the database:",
        error,
      );
    }
  };

  const handleFetchRecommendations = async (movie) => {
    setSelectedMovie(movie);
    try {
      const response = await axios.get(
        `${API_URL}/movies/${movie.id}/recommendations?top_n=10`,
      );
      setRecommendations(response.data);
    } catch (error) {
      console.error(
        "Error occurred while calculating recommendations in the backend:",
        error,
      );
      setRecommendations([]);
    }
  };

  return (
    <div className="app-container">
      <h1>🎬 Personalized Movie Recommendation Platform</h1>

      <div className="main-content-two-columns">
        {/* COLOANA 1: LISTA COMPLETĂ DE FILME POPULATE AUTOMAT */}
        <div className="card list-section">
          <h2>All Movies ({movies.length})</h2>
          <div className="movie-grid">
            {movies.map((movie) => (
              <div
                key={movie.id}
                className={`movie-card ${selectedMovie?.id === movie.id ? "active" : ""}`}
                onClick={() => handleFetchRecommendations(movie)}
              >
                <h3>{movie.title}</h3>
                <span className="badge">{movie.genre}</span>
                <p>
                  {movie.description
                    ? movie.description.substring(0, 90) + "..."
                    : "No description available."}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* COLOANA 2: RECOMANDĂRI GENERATE DE MODELUL ML */}
        <div className="card recommendations-section">
          <h2>
            Recommendations for: {selectedMovie ? selectedMovie.title : "..."}
          </h2>
          {selectedMovie ? (
            <div className="rec-grid">
              {recommendations.length > 0 ? (
                recommendations.map((rec) => (
                  <div key={rec.id} className="rec-card">
                    <h4>{rec.title}</h4>
                    <span className="badge-rec">{rec.genre}</span>
                    <p>{rec.description || "No description available."}</p>
                  </div>
                ))
              ) : (
                <p>
                  No mathematical recommendations found that are sufficiently
                  close.
                </p>
              )}
            </div>
          ) : (
            <p className="hint">
              Select a movie from the list to activate the content-based
              filtering engine.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
