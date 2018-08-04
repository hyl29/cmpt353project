# CMPT 353 Project
# ml_movies.py
# Leo Chen
import sys
import gzip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import seaborn
seaborn.set()

def sum_nums(line):
    nums = re.findall(r'\d+',line) #regex find numbers
    nums = list(map(int, nums)) #to int datatype
    sums = np.sum(nums)
    return sums
    

def main():
    #genres_fh = gzip.open('genres.json.gz')
    omdb_data_fh = gzip.open('omdb-data.json.gz')
    rotten_tomatoes_fh = gzip.open('rotten-tomatoes.json.gz')
    wikidata_movies_fh = gzip.open('wikidata-movies.json.gz')
    
    #genres = pd.read_json(genres_fh, orient='record', lines=True)
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

    #filter 
    movies = movies.dropna(subset=['omdb_awards'])
    movies = movies[movies['omdb_awards'] != 'N/A']
    movies['total_awards'] = movies['omdb_awards'].apply(lambda x: sum_nums(x)) #regex and sum
    movies = movies.drop(columns=['country_of_origin','enwiki_title',\
                                  'genre','imdb_id','label','omdb_plot',\
                                  'original_language','publication_date',\
                                  'rotten_tomatoes_id_x','wikidata_id',\
                                  'rotten_tomatoes_id_y','omdb_awards'])
    movies = movies.dropna()

    print(movies)
    print(movies['audience_average'].values)

    ######################## ML stuff ###########################################
    X = movies[['audience_percent','audience_ratings',\
                'critic_average','critic_percent','total_awards']].values
    y = movies['audience_average'].values
    y = y.astype('int')

    #build training set
    X_train, X_test, y_train, y_test = train_test_split(X,y)

    #bayes
    bayes_model = GaussianNB()
    bayes_model.fit(X_train, y_train)
    #bayes accuracy
    y_predicted = bayes_model.predict(X_test)
    print(accuracy_score(y_test, y_predicted))

    #knn
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X_train, y_train)
    #knn accuracy
    y_predicted = knn_model.predict(X_test)
    print(accuracy_score(y_test, y_predicted))

##    #svc
##    svc_model = SVC(kernel='linear',C=1)
##    svc_model.fit(X_train, y_train)
##    #svc accuracy
##    y_predicted = svc_model.predict(X_test)
##    print(accuracy_score(y_test, y_predicted))

if __name__ == '__main__':
    main()


