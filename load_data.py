import requests
import shutil
import pandas as pd
import re


def download_data(url):
    req = requests.get(url)
    filename = url.split('/')[-1]

    with open(filename, 'wb') as output_file:
        output_file.write(req.content)

    shutil.unpack_archive(filename)
    print('Download completed')


def create_dataframes():
    df_ratings = pd.read_csv('BX-Book-Ratings.csv',
                             encoding='unicode_escape', sep=';')
    df_users = pd.read_csv('BX-Users.csv', encoding='unicode_escape', sep=';')

    with open('BX-Books.csv', 'r') as infile, open('BX-Books_adj.csv', 'w') as outfile:
        for line in infile:
            line = re.sub(';[^"]', ',', line)
            outfile.write(line)

    df_books = pd.read_csv(
        'BX-Books_adj.csv', encoding='unicode_escape', sep=';')

    return df_ratings, df_users, df_books
