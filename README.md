# Movie Reccommendation App
Welcome to **Movie Recommendation App.** This project was made for estimate which movie or movies can a user should watch depending on two **recommendation models**:
* Content Based: which chooses one or more movies to the user deppending on some features of the movie, like genres, cast, director and overview.
* Collaborative Filtering: suggest same one o more movies but deppending on the user's score on each movie he/she has watched.
  
(Click on the image below to go to the app website.)
 
[![movieRecommendation](sitio.png)](https://movierecommendationpy.streamlit.app)

## Technical context:
**Content Based:** this model was developed with a scikit-learn function named cosine_similarity, which assigns a value to every string (movie features) and then generate a squared matrix with values for every single movie where the more value, the more similarity between the movie.

**Collaborative Filtering:** this model uses the surprise python library to get the SVD (Single Value Decomposition) to train the model between the watched movies by the user with his/her score and the other users watched movies and their score to that movies.





