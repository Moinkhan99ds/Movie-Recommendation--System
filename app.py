import streamlit as st
import pickle
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="🎬 Movie Recommender",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.markdown("Get similar movies using Machine Learning 🚀")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()

# ------------------ FUNCTION ------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    
    return recommended_movies

# ------------------ UI ------------------
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie", movie_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    
    st.subheader(" Top Recommendations")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(f"{recommendations[idx]}")
            st.write(" Similar Movie")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
