import pickle
import pandas as pd
import json
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
from surprise import Reader, Dataset, SVD, evaluate


def get_director(x):
	for i in x:
		if i['job'] == 'Director':
			return i['name']
	return ''

def get_list(x):
	if isinstance(x, list):
		name = [i['name'] for i in x]
		if len(name) > 3:
			names = name[:3]
		return name
	return []

def clean_data(x):
	if isinstance (x, list):
		return [str.lower(i.replace(" ","")) for i in x]
	else:
		if isinstance (x, str):
			return str.lower(x.replace(" ",""))
		else:
			return ""

def check(x, ID):
	if x['movieId'] in ID:
		return np.nan
	else:
		return x['movieId']

file=open('moviedata.bin','rb')
movies=pickle.load(file)
file.close()


def train_other_model(movies):
	features=['cast', 'crew', 'keywords', 'genres']
	for feature in features:
		movies[feature]=movies[feature].apply(literal_eval)
	movies['director'] = movies['crew'].apply(get_director)
	for feature in features:
		movies[feature] = movies[feature].apply(get_list)
	for feature in features:
		movies[feature] = movies[feature].apply(clean_data)
	movies['keywords1']=movies['keywords'].apply(lambda x: ' '.join(x))
	movies['cast1']=movies['cast'].apply(lambda x: ' '.join(x))
	movies['genres1']=movies['genres'].apply(lambda x: ' '.join(x))
	movies['soup']=movies['keywords1']+" "+movies['cast1']+" "+movies['director']+" "+movies['director']+" "+movies['genres1']+" "+movies['cast1'].map(str)
	#get model
	count = CountVectorizer(stop_words='english')
	count_matrix = count.fit_transform(movies['soup'])
	cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
	return cosine_sim2


def train_user_base(movies):
	reader = Reader()
	ratings = pd.read_csv('ratings_small.csv')
	data = Dataset.load_from_df(ratings[['userId','movieId','rating']],reader)
	data.split(n_folds=5)
	svd = SVD()
	trainset = data.build_full_trainset()
	svd.fit(trainset)
	return svd

import os.path
file_path = './user.bin'
n_bytes = 2**31
max_bytes = 2**31 - 1
data = train_user_base(movies)

bytes_out = pickle.dumps(data,protocol=4)
with open(file_path, 'wb') as f_out:
	for idx in range(0, len(bytes_out), max_bytes):
		f_out.write(bytes_out[idx:idx+max_bytes])
