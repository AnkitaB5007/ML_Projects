import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('/ds/text/netflix/movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity_dict = pickle.load(open('/ds/text/netflix/movies_similarity.pkl', 'rb'))
movies_similarity = pd.DataFrame(similarity_dict)

def get_posters(movie_name):
    data = requests.get('https://www.omdbapi.com/?t={}&apikey=8fe16ef5'.format(movie_name)).json()
    if data['Response'] == 'True':
        return data['Poster']
    else:
        return 'https://www.123moviesfree.net/wp-content/uploads/2018/03/no-poster.jpg'
    
    
    
def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances_array = movies_similarity[movie_index]
    similar_5_movies = sorted(list(enumerate(distances_array)), reverse= True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for idx in similar_5_movies:
        recommended_movies.append(movies.iloc[idx[0]]['title'])
        recommended_movies_posters.append(get_posters(movies.iloc[idx[0]]['title']))
    return recommended_movies, recommended_movies_posters

st.title("Netflix Recommendation")

option = st.selectbox(
    "Select a movie",
    movies['title'].values,
)
st.write("You selected:", option)

if st.button('Recommend'):
    rec_movies, posters = recommend(option)
    st.write("Recommended movies:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.write(rec_movies[0])
    with col2:
        st.image(posters[1])
        st.write(rec_movies[1])
    with col3:
        st.image(posters[2])
        st.write(rec_movies[2])
    with col4:
        st.image(posters[3])
        st.write(rec_movies[3])
    with col5:
        st.image(posters[4])
        st.write(rec_movies[4])
        
        