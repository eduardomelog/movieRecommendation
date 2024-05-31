import streamlit as st
import numpy as np
import pandas as pd


# FIRST PAGE SETTINGS
similarity_matrix = np.load('similarity_matrix.npy')
indices = pd.read_pickle('indices.pkl')
df2 = pd.DataFrame(indices).reset_index()
df2.columns = ['title', 'index']

def get_recommendations(title, cosine_sim=similarity_matrix):
    # Obtiene el indice que coincide con el título
    idx = indices[title]

    # Conseguimos los pares de similaridades entre todas las peliculas con esa pelicula
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenamos las películas segun su puntaje de similaridad
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Hacemos un top 10
    sim_scores = sim_scores[1:6]

    # Obtenemos los índices de esas películas
    movie_indices = [i[0] for i in sim_scores]

    # Devolvemos el listado
    return df2['title'].iloc[movie_indices]
# END FIRST PAGE SETTINGS



def get_recommendations2(title, cosine_sim=similarity_matrix):
    # Obtiene el indice que coincide con el título
    idx = indices[title]

    # Conseguimos los pares de similaridades entre todas las peliculas con esa pelicula
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenamos las películas segun su puntaje de similaridad
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Hacemos un top 10
    sim_scores = sim_scores[1:6]

    # Obtenemos los índices de esas películas
    movie_indices = [i[0] for i in sim_scores]

    # Devolvemos el listado
    df = df2['title'].iloc[movie_indices].to_frame()
    df.columns = ['Title']
    df['Score'] = [str(round(x[1] * 100, 2)) + '%' for x in sim_scores]
    df.index = [1,2,3,4,5]
    return df






# APP DEPLOYMENT
st.title("Movie Recommendation Models")

st.image('movies.jpg',
        #style = 'display: block; margin:auto;'
             )

# Crea las pestañas
tab1, tab2 = st.tabs(["Content Based Model", "Pestaña 2"])

# Contenido de la Pestaña 1
with tab1:
    st.write('This model was made using the cosine similarity between some movie features such as the review, cast, gender and director.')
    movie = st.selectbox('Select a movie', sorted(df2['title']))
    if st.button('Recommend Movies'):
        df = get_recommendations2(movie)
        st.write(df)
        

# Contenido de la Pestaña 2
with tab2:
    st.header("Bienvenido a la Pestaña 2")
    st.write("Este es el contenido de la segunda pestaña.")
    st.line_chart({"data": [1, 5, 2, 6, 8, 3]})
