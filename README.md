# Personalized Movie Recommendation Platform

A Full-Stack movie discovery and recommendation ecosystem designed to deliver real-time, personalized content suggestions. The platform integrates a modern web architecture with an embedded Machine Learning pipeline, moving away from isolated notebooks into a production-ready application.

> **Current Status:** Phase 1 (MVP) is fully functional featuring an active Content-Based Filtering engine, production database seeding via the TMDb API, and a clean two-column React frontend.

---

## Architecture & Tech Stack

### Frontend

- **React 18 (Vite):** Fast, modern UI built with high-performance state management (`useState`, `useEffect`).
- **Axios:** Handles asynchronous HTTP requests to the backend API.
- **Modern CSS:** Adaptive Dark-Mode interface optimized for content discovery.

### Backend & Machine Learning

- **FastAPI:** High-performance, production-ready Python web framework.
- **SQLAlchemy (ORM):** Object-Relational Mapping for secure, structured database transactions.
- **PostgreSQL (Docker):** Relational database storage for users and movie metadata.
- **Scikit-Learn & Pandas:** Powers the TF-IDF Vectorizer and Cosine Similarity computations.

---

## The ML Engine (How it works right now)

The current recommendation system utilizes **Content-Based Filtering**.

1. **Feature Engineering:** Movie genres and textual overviews are combined and processed.
2. **Vectorization:** A `TfidfVectorizer` transforms text into dense numerical vectors, eliminating common stop words and highlighting unique keywords.
3. **Similarity Computation:** A `cosine_similarity` matrix evaluates the mathematical distance between vectors.
4. **Real-Time Delivery:** When a user selects a movie, the FastAPI endpoint queries the matrix and returns the top 3 closest matching films directly from PostgreSQL within milliseconds.

---

## Installation & Local Setup

### Prerequisites

- Python 3.10+
- Node.js (LTS v20+)
- Docker Desktop

### 1. Database Setup (PostgreSQL via Docker)

````bash
docker run -d --name movie-postgres -e POSTGRES_USER=horia -e POSTGRES_PASSWORD=Rapid1923 -e POSTGRES_DB=moviedb -p 5432:5432 postgres

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
.venv/Scripts/Activate.ps1

pip install "fastapi[standard]" sqlalchemy psycopg2-binary pydantic pandas numpy scikit-learn requests uvicorn
````

To run the backend server:

```bash
python -m uvicorn app.main:app --reload
```

### 3. Seeding Data

Add your TMDb API key inside backend/app/seed_movies.py and run:

```bash
python app/seed_movies.py
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser to access the application.

## Project Roadmap

This project is This project is actively developed. The core data pipeline is established, paving the way for the following production features:

- **User Authentication & Profiles:** Personalized watchlists and user-specific recommendations.
- **Hybrid Recommendation System:** Integration of Collaborative Filtering to complement the existing Content-Based approach.
- **Admin Dashboard:** For managing movie metadata, user activity, and system analytics.
- **Unit and Integration Testing:** Ensuring robustness and reliability of the recommendation engine and API endpoints.

## License

This project is open-source and available under the MIT License.
