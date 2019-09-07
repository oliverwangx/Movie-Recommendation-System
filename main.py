import pickle

import pandas as pd
import json
import numpy as np
import os.path



def check(x, ID):
	if x['movieId'] in ID:
		return np.nan
	else:
		return x['movieId']


def get_recommendations(title, cosine_sim, indices, movies):
	idx = indices[title]   
	sim_scores = list(enumerate(cosine_sim[idx]))
	sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True)
	sim_scores = sim_scores[1:9]
	movie_indices=[i[0] for i in sim_scores]
	titles=movies['title'].iloc[movie_indices]
	title_list = []
	for i in titles.index:
		title_list.append(titles[i])
	return title_list


def recommend_overview_based(title):
	indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
	titles = get_recommendations(title,cosine_sim,indices,movies)
	return titles

def recommend_other_based(title):
	indices = pd.Series(movies.index, index=movies['title'])
	titles=get_recommendations(title, cosine_sim2 ,indices,movies)
	return titles

def recommend_user_base(id):
	indices3 = pd.Series(movies.title, index=movies.id).drop_duplicates()
	titles = []
	ID=ratings[ratings['userId']==id].movieId.tolist()
	temp=ratings.apply(lambda row: check(row,ID), axis=1).dropna().drop_duplicates()
	k=[]
	for item in temp.tolist():
		k.append([item,svd.predict(id,item,3).est] )
	k1=sorted(k, key = lambda x: x[1], reverse=True)
	t=[]
	for item in k1:
		try:
			t.append([int(item[0]), indices3[int(item[0])]])
		except:
			continue
	for i in range(0,8):
		titles.append(t[i][1])
	return titles

#load first file
file=open('moviedata.bin','rb')
movies=pickle.load(file)
file.close()

#load second file
file_path = './overview.bin'
n_bytes = 2**31
max_bytes = 2**31 - 1

bytes_in = bytearray(0)
input_size = os.path.getsize(file_path)
with open(file_path, 'rb') as f_in:
	for _ in range(0, input_size, max_bytes):
		bytes_in += f_in.read(max_bytes)
cosine_sim = pickle.loads(bytes_in)

#load third file
file_path = './other.bin'
n_bytes = 2**31
max_bytes = 2**31 - 1

bytes_in = bytearray(0)
input_size = os.path.getsize(file_path)
with open(file_path, 'rb') as f_in:
	for _ in range(0, input_size, max_bytes):
		bytes_in += f_in.read(max_bytes)
cosine_sim2 = pickle.loads(bytes_in)


#load last file
file=open('user.bin','rb')
svd=pickle.load(file)
file.close()

#load for users
ratings = pd.read_csv('ratings_small.csv')


print("overview: ", recommend_overview_based('The Dark Knight Rises'))
print("other: ",recommend_other_based('The Dark Knight Rises'))
print("user 1: ", recommend_user_base(1))
print("user 2: ", recommend_user_base(2))
print("user 3: ", recommend_user_base(3))
print("user 4: ", recommend_user_base(4))
print("user 5: ", recommend_user_base(5))
print("user 6: ", recommend_user_base(6))
print("user 7: ", recommend_user_base(7))
print("user 8: ", recommend_user_base(8))
print("user 9: ", recommend_user_base(9))
print("user 10: ", recommend_user_base(10))