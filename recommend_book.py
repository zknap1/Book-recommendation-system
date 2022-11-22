import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def get_books_by_keyword(data, keyword:str, n:int):

    # tokenize each title and return document term matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_title = vectorizer.fit_transform(data['Book-Title'])

    # transform keyword to dtm
    query_vec = vectorizer.transform([keyword])

    # calculate cosine similarities
    results = cosine_similarity(query_vec, tfidf_matrix_title).flatten()

    df_results = pd.DataFrame(
        results, columns=['Similarity-Score']).reset_index()
    if 'index' not in data.columns:
        data = data.reset_index()

    # merge calculated similarities with titles
    df_results_merged = pd.merge(data, df_results, on='index')

    return df_results_merged.sort_values(by='Similarity-Score', ascending=False).head(n)


def frequency_table(table, column):

    # calcualte relative and absolute frequencies
    freq_table = pd.concat([table[column].value_counts(),
                            table[column].value_counts(normalize=True)*100], axis=1)
    freq_table.columns = ['AbsFreq', 'Proportion [%]']
    freq_table.sort_index(ascending=True, inplace=True)
    return freq_table


def get_books_based_on_author(data, author):

    # search for books based on author
    author_search_result = data['Book-Author'].str.contains(
        str('.*(\W?'+author+'\W?).*'),
        regex=True)
    return data[author_search_result]


def get_top_rated_books(original_data):

    new_data = original_data.sort_values(
        by='Book-Rating', ascending=False).reset_index()
    new_data.drop_duplicates(subset=['Book-Title'], inplace=True)

    titles_to_remove = []

    for i in list(new_data['Book-Title']):
        for j in list(new_data['Book-Title']):
            if i != j and i.lower() in j.lower():
                titles_to_remove.append(j)

    return new_data[~new_data['Book-Title'].isin(titles_to_remove)]


def get_books_based_on_popularity(data, title):
    # filter users who rated the book with rating > 5
    users_ID = data[(data['Book-Title'] == title)
                    & (data['Book-Rating'] > 5)]['User-ID']
    users_data = pd.merge(users_ID, data, on='User-ID',
                          how='inner')

    # check which other books they read the most                      
    df = users_data.groupby(
        by=['Book-Title', 'Book-Author'])['Book-Rating'].count().reset_index()
    df = df[df['Book-Title'] != title]
    result = df.sort_values(by='Book-Rating', ascending=False)
    return result


def recommend_book_by_author(data, author: str):
    input_data = get_books_based_on_author(data, author)
    df_books_by_author = get_top_rated_books(input_data)
    return df_books_by_author['Book-Title']


def recommend_book_by_keyword(data, keyword: str, n: int):
    result = get_books_by_keyword(data, keyword, n)
    book_rec = get_top_rated_books(result)
    return book_rec[['Book-Title', 'Book-Author']]


def recommend_book_by_popularity(data_unique, data_all, title: str):
    df_title = get_books_by_keyword(data_unique, title, 1)
    book_rec = get_books_based_on_popularity(
        data_all, df_title['Book-Title'].values[0])
    return book_rec[['Book-Title', 'Book-Author']]


def recommend_by_author_and_keyword(data, author, keyword, n):
    response_author = recommend_book_by_author(data, author)
    df_response_author = pd.DataFrame(response_author, columns=['Book-Title'])
    df_response_author = df_response_author.reset_index(drop=True)
    result = get_books_by_keyword(df_response_author, keyword, n)
    result_top = result.sort_values(by='Similarity-Score', ascending=False)
    return result_top['Book-Title']
