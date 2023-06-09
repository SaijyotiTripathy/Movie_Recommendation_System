import pickle
import requests
import streamlit as st

def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?id={}".format(file_id)
    response = requests.get(URL)
    with open(destination, "wb") as f:
        f.write(response.content)

def load_similarity(file_path):
    with open(file_path, "rb") as f:
        similarity = pickle.load(f)
    return similarity
        
        
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = list(movies['title'].values()).index(movie)
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies['movie_id'][i[0]]
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies['title'][i[0]])

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')

# Load movie_list.pkl from GitHub
movies = st.cache(pickle.load)(open('movie_dict.pkl', 'rb'))

# Specify the file ID of the similarity.pkl file in your Google Drive
file_id = "1iEdX1JcjJdT2HYiNKmeJMKf9bpSEj07c"

# Define the destination path where you want to save the file
destination_path = "similarity.pkl"

# Download the file from Google Drive
download_file_from_google_drive(file_id, destination_path)

# Load the similarity.pkl file
similarity = load_similarity(destination_path)

movie_list = list(movies['title'].values())
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    #recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    recommended_movie_names = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.beta_columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        #st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        #st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        #st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        #st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        #st.image(recommended_movie_posters[4])
        
if st.button('Show Similarity Matrix'):
    st.write(similarity)
