import streamlit as st
import pickle

# ------------------ PAGE ------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")
st.write("ML-powered movie recommendations ")

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
        return ["Movie not found"]

    cluster = movies[movies['title'] == movie_title]['cluster'].values[0]
    similar = movies[movies['cluster'] == cluster]['title'].values

    return [m for m in similar if m != movie_title][:5]

# ------------------ UI ------------------
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

if st.button("Recommend"):
    results = recommend(selected_movie)

    st.subheader("🔥 Top Recommendations")

    cols = st.columns(5)
    for i in range(len(results)):
        with cols[i]:
            st.write(results[i])

# ------------------ FOOTER ------------------
st.markdown("---")
st.write("Built with Streamlit")
