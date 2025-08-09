import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables (optional for local dev)
load_dotenv()

# Securely fetch the API key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Never hardcode secrets in code
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# Load saved artifacts
movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

def fetch_poster_path(movie_id):
    """Fetch poster path from TMDB API given a movie_id."""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('poster_path', '')
    except Exception as e:
        st.warning(f"Could not fetch poster for movie ID {movie_id}: {e}")
        return ''

def recommend(movie, top_n=5):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return []

    idx = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]

    recommended = []
    for i in movie_list:
        row = movies.iloc[i[0]]
        title = row['title']
        movie_id = row.get('movie_id', None)
        poster_path = ''
        if movie_id:
            poster_path = fetch_poster_path(movie_id)
        poster_url = f"{BASE_IMAGE_URL}{poster_path}" if poster_path else None
        recommended.append((title, poster_url))
    return recommended

# Streamlit UI
st.set_page_config(page_title="MovieMatch+", layout="wide")

# Centered header
st.markdown("""
    <div style='text-align: center;'>
        <h1>🎬 MovieMatch+</h1>
        <h3>Smart Recommendations with Live Posters</h3>
        <p><em>Your next favorite movie is just a click away.</em></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Movie selection
selected_movie = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader("Top Recommendations:")
        cols = st.columns(len(recommendations))
        for idx, (title, poster_url) in enumerate(recommendations):
            with cols[idx]:
                if poster_url:
                    st.image(poster_url, width=180)
                else:
                    st.text("No poster available")
                st.caption(title)
    else:
        st.warning("Movie not found or not enough data.")
