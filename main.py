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
# END FIRST PAGE SETTINGS






# SECOND PAGE SETTINGS
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
reader = Reader()
ratings = pd.read_csv('ratings.csv')
ratings = ratings[ratings['original_title'].str.contains(r'^[a-zA-Z0-9 ]*$', na=False)]
ratings.head()

data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

svd = SVD()
#cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

trainset = data.build_full_trainset()
svd.fit(trainset)

def recomendacion (uid):
  lista_no_vistos = ratings[~ratings['movieId'].isin(ratings[ratings['userId'] == uid].movieId)][['movieId','original_title']].drop_duplicates()
  recomendaciones = []
  for ind in lista_no_vistos.index:
    prediction= svd.predict(uid, lista_no_vistos['movieId'][ind])
    pred_item, pred_est = prediction.iid, prediction.est
    recomendacion = [pred_item, pred_est]
    recomendaciones.append(recomendacion)
  recomendaciones = pd.DataFrame(recomendaciones, columns=['movieId','rating_est'])
  recomendaciones = recomendaciones.merge(lista_no_vistos).sort_values(by='rating_est', ascending=False)
  return recomendaciones.head(5)
# EN SECOND PAGE SETTINGS







# APP DEPLOYMENT
st.title("Movie Recommendation Models")
st.markdown(f'###### [Click here to go to the GitHub repository.](https://github.com/eduardomelog/movieRecommendation)')


st.image('movies.jpg',
        #style = 'display: block; margin:auto;'
             )

# Crea las pestañas
tab1, tab2 = st.tabs(["Content Based Model", "Collaborative Filtering"])

# Contenido de la Pestaña 1
with tab1:
    movie = st.selectbox('Select a movie', sorted(df2['title']))
    if st.button('Recommend Movies'):
        df = get_recommendations2(movie)
        st.write(df)
        

# Contenido de la Pestaña 2
with tab2:
    userid = st.selectbox('Select an user ID', range(1,80))
    if st.button('Recommend Movies '):
        watched_movies = ratings[ratings['userId'] == userid].sort_values(['rating'], ascending = False)[['original_title','rating']]
        watched_movies.columns = ['Title', 'Users rating']
        st.write('Watched movies by this user:')
        st.write(watched_movies)
        
        df = recomendacion(userid)
        df = df[['original_title', 'rating_est']]
        df.columns = ['Title', 'Score']
        df.index = [1,2,3,4,5]
        st.write('Movies that this user should watch:')
        st.write(df)
    
