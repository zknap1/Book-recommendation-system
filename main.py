import numpy as np
import pandas as pd
from load_data import download_data, create_dataframes
from prepare_data import clean_merge


# download zip file
url= 'http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip'
download_data(url)

# load and unzip csv files
df_ratings, df_users, df_books = create_dataframes()

# data preparation  
clean_merge(df_ratings, df_users, df_books)
