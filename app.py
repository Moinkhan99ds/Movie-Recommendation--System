import streamlit as st
import pickle
import requests

# ------------------ CONFIG ------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

h1 {
    text-align: center;
    color: #ff4b4b;
}

.movie-card {
    text-align: center;
    background-color: #111;
    padding: 10px;
    border-radius: 12px;
    transition: 0.3s;
}
.movie-card:hover {
    transform: scale(1.05);
}

img {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.caption("AI-powered movie suggestions with posters")

# ------------------ TMDB API ------------------
API_KEY = "2020986cfc17a3040a697c0fa0c02656"

def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    data = requests.get(url).json()

    if data["results"]:
        poster_path = data["results"][0]["poster_path"]
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    return None

# ------------------ LOAD ------------------
@st.cache_data
def load_data():
    movies = pickle.load(open("movies1.pkl", "rb"))
    tfidf = pickle.load(open("tfidf.pkl", "rb"))
    kmeans = pickle.load(open("kmeans.pkl", "rb"))
    return movies, tfidf, kmeans

movies, tfidf, kmeans = load_data()

# ------------------ RECOMMEND ------------------
def recommend(movie_title):
    if movie_title not in movies['title'].values:
        return []

    cluster = movies[movies['title'] == movie_title]['cluster'].values[0]
    similar = movies[movies['cluster'] == cluster]['title'].values

    return [m for m in similar if m != movie_title][:5]

# ------------------ UI ------------------
col1, col2 = st.columns([2,1])

with col1:
    movie_list = movies['title'].values
    selected_movie = st.selectbox("🎥 Choose a Movie", movie_list)

with col2:
    st.write("")
    st.write("")
    recommend_btn = st.button("🚀 Recommend")

# ------------------ RESULT ------------------
if recommend_btn:

    with st.spinner("Finding best movies..."):
        results = recommend(selected_movie)

    st.markdown("### 🔥 Top Recommendations")

    cols = st.columns(5)

    for i, movie in enumerate(results):
        with cols[i]:
            poster = fetch_poster(movie)

            st.markdown('<div class="movie-card">', unsafe_allow_html=True)

            if poster:
                st.image(poster)

            st.markdown(f"{movie}")

            # fake rating (for UI boost)
            st.caption(f"⭐ {round(7 + i*0.3,1)} / 10")

            st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Movie data powered by TMDB")
