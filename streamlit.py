import pickle
import requests
import streamlit as st
import gdown

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
    #recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies['movie_id'][i[0]]
       # recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies['title'][i[0]])

    #return recommended_movie_names,recommended_movie_posters
    return recommended_movie_names


st.header('Movie Recommender System')

# Mount Google Drive
drive.mount('/content/drive')

# Load movie_list.pkl from GitHub
movies = st.cache(pickle.load)(open('movie_dict.pkl', 'rb'))

# Load similarity.pkl from Google Drive
similarity_url = "https://drive.google.com/uc?id=1iEdX1JcjJdT2HYiNKmeJMKf9bpSEj07c"
output_file = "similarity.pkl"
gdown.download(similarity_url, output_file, quiet=False)

# Load similarity.pkl
similarity = pickle.load(open(output_file, 'rb'))

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
