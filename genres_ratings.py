# CMPT 353 Project
# genres_ratings.py
# Leo Chen
import sys
import gzip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re
import seaborn
seaborn.set()

def get_genre_rating(row):
    #print(row['omdb_genres'])
    df = pd.DataFrame({'genres':row['omdb_genres']})
    print(df)

def main():
    genres_fh = gzip.open('genres.json.gz')
    omdb_data_fh = gzip.open('omdb-data.json.gz')
    rotten_tomatoes_fh = gzip.open('rotten-tomatoes.json.gz')
    wikidata_movies_fh = gzip.open('wikidata-movies.json.gz')
    
    genres = pd.read_json(genres_fh, orient='record', lines=True)
    omdb_data = pd.read_json(omdb_data_fh, orient='record', lines=True)
    rotten_tomatoes = pd.read_json(rotten_tomatoes_fh, orient='record', lines=True)
    wikidata_movies = pd.read_json(wikidata_movies_fh, orient='record', lines=True)\
                    .drop(columns=['based_on','cast_member',\
                                   'director','made_profit',\
                                   'main_subject','series',\
                                   'filming_location','metacritic_id'])
    
    #combine all data into one df
    movies = wikidata_movies.merge(rotten_tomatoes, how='outer', on='imdb_id')
    movies = movies.merge(omdb_data, how='outer', on='imdb_id')


    #filter data
    genres_ratings = movies[['omdb_genres','critic_average','audience_average']].dropna()
    genres_ratings['audience_average'] = genres_ratings['audience_average']*2

    #audience
    genres_audience = pd.DataFrame({'avg_audience_rating':np.repeat(genres_ratings['audience_average'].values,\
                    genres_ratings['omdb_genres'].str.len()),\
                    'omdb_genres':np.concatenate(genres_ratings['omdb_genres'].values)}) #list to col
    genres_audience = genres_audience[genres_audience['omdb_genres'] != 'N/A'] #get rid of NA
    genres_audience = genres_audience.groupby('omdb_genres').mean().reset_index()
    genres_audience = genres_audience.sort_index()

    #critic
    genres_critic = pd.DataFrame({'avg_critic_rating':np.repeat(genres_ratings['critic_average'].values,\
                    genres_ratings['omdb_genres'].str.len()),\
                    'omdb_genres':np.concatenate(genres_ratings['omdb_genres'].values)}) #list to col
    genres_critic = genres_critic[genres_critic['omdb_genres'] != 'N/A'] #get rid of NA
    genres_critic = genres_critic.groupby('omdb_genres').mean().reset_index()
    genres_critic = genres_critic.sort_index()

    #combine
    genres_audience['avg_critic_rating'] = genres_critic['avg_critic_rating']
    genres_combined = genres_audience
    print(genres_combined)

    ################# PLOT #############################################################
    plt.bar(genres_combined['omdb_genres'],genres_combined['avg_audience_rating'],color = 'blue', alpha=0.5, label='audience')
    plt.bar(genres_combined['omdb_genres'],genres_combined['avg_critic_rating'],color = 'red', alpha=0.5, label='critic')
    plt.legend()
    plt.title('Genres vs Ratings')
    plt.xticks(rotation=40)
    plt.show()
    
if __name__ == '__main__':
    main()
















    
