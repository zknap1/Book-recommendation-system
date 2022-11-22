import pickle
from recommend_book import frequency_table
import numpy as np
import pandas as pd


def clean_merge(df_ratings, df_users, df_books):
    # remove implicit ratings
    df_ratings = df_ratings[df_ratings['Book-Rating'] > 0]

    # replace missin values with median
    df_users['Age'].fillna(df_users['Age'].median(), inplace=True)
    df_books['Book-Author'].fillna('Other', inplace=True)

    # replace outliers
    age_q = df_users['Age'].quantile(0.998)
    df_users['Age'].mask(df_users['Age'] > age_q, age_q, inplace=True)

    # number of ratings per user
    print(frequency_table(df_ratings, 'Book-Rating'))

    df_ratings_grouped = df_ratings.groupby(['User-ID'])['Book-Rating'].count()
    df_ratings_grouped.describe()

    # merge tables
    data = pd.merge(df_books[['Book-Author', 'ISBN', 'Book-Title']], df_ratings, on='ISBN',
                    how='inner')
    data['Book-Author'] = data['Book-Author'].str.title()
    data = data.replace('&amp,', '& ', regex=True)

    # consider books with more than 3 ratings
    data_adj = data.groupby(['Book-Title'])['Book-Rating'].count().reset_index(
        name='Count')
    data_adj_merged = pd.merge(
        data, data_adj[data_adj['Count'] > 3], on='Book-Title', how='inner')
    data_adj_transformed = data_adj_merged.groupby(
        by=['Book-Title', 'Book-Author'])['Book-Rating'].mean().reset_index()

    # save data for further use
    pickle.dump(data_adj_transformed, open('data_rated', 'wb'))
    pickle.dump(data_adj_merged, open('data_popular_books', 'wb'))

    print("Preparation complete.")
