import streamlit as st
import pickle

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.title("🎬 Movie Recommendation System")
st.write("Find similar movies using Machine Learning 🚀")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    return movies

movies = load_data()

# ------------------ RECOMMEND FUNCTION ------------------
def recommend(movie_title):
    if movie_title not in movies['title'].values:
        return ["Movie not found!"]

    cluster_num = movies[movies['title'] == movie_title]['cluster'].values[0]
    similar_movies = movies[movies['cluster'] == cluster_num]['title'].values

    return [m for m in similar_movies if m != movie_title][:5]

# ------------------ UI ------------------
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    st.subheader(" Top Recommendations")

    col1, col2, col3, col4, col5 = st.columns(5)

    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(f"{recommendations[idx]}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
