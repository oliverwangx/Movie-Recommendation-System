# Movie-Recommendation-System


In this project, I describe the approaches to a customized movie recommendation. We use content filtering and collaborative fil- tering to implement the recommendation mechanism. In terms of content-based filtering, we choose Tfidf Vectorizer to extract TF-IDF feature from overview of movies, and we choose CountVectorizer for a collection of director, cast, keyword and genre. We use SVD model for collaborative-based filtering. Also, we also use Flask as the web frame, together with html to implement the front end. User can type in their ID in the first search box, or type a keyword in the second search box and select a radio to choose whether you want to search based on overview or other dimension such as director, and the system will return top eight recommended movies based on your profile, or your keyword type. With Root-mean-square error(RMSE) method, our recommendation system can reach good evaluation result of 0.9.

![image](https://github.com/lexsaints/powershell/blob/master/IMG/ps2.png)
