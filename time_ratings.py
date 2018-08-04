# CMPT 353 Project
# time_ratings.py
# Leo Chen
import sys
import gzip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re
import datetime as dt
import seaborn
seaborn.set()

def to_timestamp(date):
    return date.timestamp()

def p_test(p_value):
    print("p value:", p_value)
    if p_value < 0.05:
        print("p value < 0.05 so we can reject the null hypothesis. Therefore, the slope is different from zero.")
    else:
        print("p value >= 0.05 so we can accept the null hypothesis. Therefore, the slope is zero.")

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
    movies['audience_average']=movies['audience_average']*2

    #filter time
    movies = movies.dropna(subset=['publication_date'])
    #movies = movies.sort_values(by=['publication_date'])
    movies['publication_date'] = pd.to_datetime(movies['publication_date'])
    movies = movies[movies['publication_date'] >= '1930-01-01']

    time_ratings = movies[['publication_date','audience_average','critic_average']]

    #filter ratings
    time_ratings = time_ratings.dropna(subset=['critic_average','audience_average'])

    #Best fit line
    time_ratings['timestamp'] = time_ratings['publication_date'].apply(to_timestamp)
    slope_a, intercept_a, r_value_a, p_value_a, std_err_a = stats.linregress(time_ratings['timestamp'].values, time_ratings['audience_average'].values)
    slope_c, intercept_c, r_value_c, p_value_c, std_err_c = stats.linregress(time_ratings['timestamp'].values, time_ratings['critic_average'].values)

    ###################### plot ###########################################################################################
    plt.plot(time_ratings['publication_date'].values, time_ratings['audience_average'].values, 'b.', alpha=0.5)
    plt.plot(time_ratings['publication_date'], time_ratings['timestamp']*slope_a + intercept_a, 'k-', linewidth=3)
    plt.xticks(rotation=30)
    plt.title('Linear Regression, Time vs Audience Ratings')
    plt.show()
    
    plt.plot(time_ratings['publication_date'].values, time_ratings['critic_average'].values, 'r.', alpha=0.5)
    plt.plot(time_ratings['publication_date'], time_ratings['timestamp']*slope_c + intercept_c, 'k-', linewidth=3)
    plt.xticks(rotation=30)
    plt.title('Linear Regression, Time vs Critic Ratings')
    plt.show()

    #p value test
    p_test(p_value_c)
    p_test(p_value_a)
    
    #histogram
    plt.hist(time_ratings['audience_average'].values - (time_ratings['timestamp']*slope_a + intercept_a), bins = np.linspace(-5, 5, num=20), color='blue')
    plt.ylabel("number of ratings")
    plt.title('Residual audience rating')
    plt.show()
    
    plt.hist(time_ratings['critic_average'].values - (time_ratings['timestamp']*slope_c + intercept_c), bins = np.linspace(-5, 5, num=20), color='red')
    plt.ylabel("number of ratings")
    plt.title('Residual critic rating')
    plt.show()

    #print(time_ratings)


    
if __name__ == '__main__':
    main()
