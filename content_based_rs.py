import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



def content_based_filtering(userid):
    ratings_df = pd.read_csv(r'ratings.csv')
    movies_df = pd.read_csv(r'movies.csv')
    tags = pd.read_csv(r'tags.csv')
    movie_ratings_df = pd.merge(ratings_df, movies_df, on='movieId')
    user_means = movie_ratings_df.groupby('userId')['rating'].mean()
    movie_ratings_df['rating'] = movie_ratings_df['rating'] - \
        movie_ratings_df['userId'].map(user_means)

    ratings_matrix = movie_ratings_df.pivot_table(
        index='userId', columns='title', values='rating')

    ratings_matrix.fillna(0, inplace=True)

    user_similarity = cosine_similarity(ratings_matrix)

    input_user = userid
    input_user = int(input_user)  # Convert input to an integer

    if input_user not in ratings_matrix.index:
        return ["Invalid user ID."]
    else:
        user_index = ratings_matrix.index.get_loc(input_user)

        weighted_sum = np.dot(user_similarity[user_index], ratings_matrix)

        sum_of_similarities = np.sum(user_similarity[user_index])

        if sum_of_similarities != 0:
            predicted_ratings = user_means[input_user] + \
                (weighted_sum / sum_of_similarities)
        else:
            predicted_ratings = np.zeros_like(user_means)

        recommendations = pd.Series(
            predicted_ratings, index=ratings_matrix.columns).sort_values(ascending=False)[:5]

        rec = []
        for movie_id in recommendations.index:
            movie_title = movies_df.loc[movies_df['title']
                                        == movie_id, 'title'].values[0]
            rec.append(movie_title)
        return rec




