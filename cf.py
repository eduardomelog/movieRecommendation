import numpy as np
import pandas as pd
import streamlit as st

from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
reader = Reader()
ratings = pd.read_csv(root + 'ratings.csv')
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

recomendacion(1)










