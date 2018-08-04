# CMPT 353 Project
# ratings_awards.py
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

def sum_nums(line):
    nums = re.findall(r'\d+',line) #regex find numbers
    nums = list(map(int, nums)) #to int datatype
    sums = np.sum(nums)
    return sums
    

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

    #filter awards
    movies = movies.dropna(subset=['omdb_awards'])
    movies = movies[movies['omdb_awards'] != 'N/A']
    movies['total_awards'] = movies['omdb_awards'].apply(lambda x: sum_nums(x)) #regex and sum

    #filter ratings
    movies = movies.dropna(subset=['audience_average','audience_percent',\
                                   'audience_ratings','critic_average',\
                                   'critic_percent'])
    movies['audience_average'] = movies['audience_average']*2 #match audience to critic ratings

    #print(movies[['audience_average','audience_percent','critic_average','critic_percent']])

    print('audiences avg = ',movies['audience_average'].mean())
    print('critics avg = ',movies['critic_average'].mean())
    
########################## PLOT #########################################
    plt.scatter(movies['audience_average'],np.sqrt(movies['total_awards']), s = 4, color = 'blue')
    plt.xlabel('Audience Avg')
    plt.ylabel('Awards & nominations')
    plt.title('Audience Avg vs Awards')
    plt.show()
##    plt.scatter(movies['audience_percent'],np.sqrt(movies['total_awards']), s = 4)
##    plt.xlabel('Audience Percent')
##    plt.ylabel('Awards & nominations')
##    plt.title('Audience Percent vs Awards')
##    plt.show()
    plt.scatter(movies['critic_average'],np.sqrt(movies['total_awards']), s = 4, color = 'red')
    plt.xlabel('Critic Avg')
    plt.ylabel('Awards & nominations')
    plt.title('Critic Avg vs Awards')
    plt.show()
##    plt.scatter(movies['critic_percent'],np.sqrt(movies['total_awards']), s = 4)
##    plt.xlabel('Critic Percent')
##    plt.ylabel('Awards & nominations')
##    plt.title('Critic Percent vs Awards')
##    plt.show()

    plt.hist(movies['audience_average'],alpha=0.5, label='audience', color = 'blue')
    plt.hist(movies['critic_average'],alpha=0.5, label='critic', color = 'red')
    plt.xlabel('ratings scale')
    plt.title('Number of ratings')
    plt.legend()
    plt.show()
    #plt.hist(movies['audience_percent'])
    #plt.hist(movies['critic_percent'])
    #plt.show()

    
if __name__ == '__main__':
    main()
