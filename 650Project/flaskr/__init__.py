from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__, template_folder='../templates')


userDict = {"1":  ['The Reluctant Debutante', 'Swimming with Sharks', 'On Our Merry Way', 'Quiz Show', 'The Aristocats', 'Candleshoe', 'The Phantom', 'The Black Hole'],
"2": ['Swimming with Sharks', 'Rare Birds', 'Carmen Miranda: Bananas Is My Business', 'The Fourth Protocol', 'Charade', "Gone Fishin'", 'The Band Wagon', 'The Reluctant Debutante'],
"3": ['Carmen Miranda: Bananas Is My Business', "Gone Fishin'", 'L.A. Story', 'Meet Me in St. Louis', "L'Enfer", 'The Reluctant Debutante', 'The Aristocats', 'Star Trek: Insurrection'],
"4": ['Serial Mom', 'Love and a .45', 'Swimming with Sharks', 'A Hungarian Fairy Tale', 'Before and After', 'L.A. Story', 'The Raven', 'Seconds'],
"5":  ['Swimming with Sharks', 'The Reluctant Debutante', 'Sleepless in Seattle', 'Human Highway', 'Heartburn', 'Sherlock Holmes and the Leading Lady', 'Star Trek: Insurrection', 'The Phantom'],
"other":  ['Inception', 'Interstellar', 'Out of the Furnace', 'Batman Begins', 'The Dark Knight', 'Charade', 'Doodlebug', 'Memento'],
"overview": ['The Dark Knight', 'Batman Forever', 'Batman Returns', 'Batman: Under the Red Hood', 'Batman', 'Batman Unmasked: The Psychology of the Dark Knight', 'Batman Beyond: Return of the Joker', 'Batman: Year One']}



picDict = {"The Reluctant Debutante":"https://m.media-amazon.com/images/M/MV5BNTE2YTY3M2ItYWVjOS00MTUxLWI5YjEtMWQwYjZjMTMwYWFkXkEyXkFqcGdeQXVyNzc5MjA3OA@@._V1_SY1000_CR0,0,648,1000_AL_.jpg",
"Swimming with Sharks":"https://m.media-amazon.com/images/M/MV5BZjNhZmVmZGQtMTQ3OS00YWEzLThjMWUtMWFiNjA3YzQ1Yjg0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
"On Our Merry Way":"https://m.media-amazon.com/images/M/MV5BYmU3OWY0NzMtNGQ5ZC00NmE1LTg1N2UtNDQ1ZGQyNzg3ZTM2XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_.jpg",
"Quiz Show":"https://m.media-amazon.com/images/M/MV5BNTYxNjdjMzUtYzAyNC00NWJhLWFlM2EtNWM4NDBhZmQ1YjJiXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SY1000_CR0,0,678,1000_AL_.jpg",
"The Aristocats":"https://m.media-amazon.com/images/M/MV5BMTU1MzM0MjcxMF5BMl5BanBnXkFtZTgwODQ0MzcxMTE@._V1_SY1000_CR0,0,674,1000_AL_.jpg",
"Candleshoe":"https://m.media-amazon.com/images/M/MV5BMDVkZjMxNjItNzM4My00ODdjLTk5YTgtNzNlMWJmZGZjNzRhXkEyXkFqcGdeQXVyNzc5MjA3OA@@._V1_SY1000_CR0,0,647,1000_AL_.jpg",
"The Phantom":"https://m.media-amazon.com/images/M/MV5BMGE3MjRhZjUtZGQ0My00ZGM4LWI4YmMtMDYwM2ZjYTQ1ZWNkL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_CR0,0,670,1000_AL_.jpg",
"The Black Hole":"https://m.media-amazon.com/images/M/MV5BMTQ3MjgzOTEyOV5BMl5BanBnXkFtZTgwOTIwNTA5NTE@._V1_.jpg",
"The Dark Knight":"https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SY1000_CR0,0,675,1000_AL_.jpg",
"Batman Forever":"https://m.media-amazon.com/images/M/MV5BNWY3M2I0YzItNzA1ZS00MzE3LThlYTEtMTg2YjNiOTYzODQ1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_CR0,0,678,1000_AL_.jpg",
"Batman Returns":"https://m.media-amazon.com/images/M/MV5BOGZmYzVkMmItM2NiOS00MDI3LWI4ZWQtMTg0YWZkODRkMmViXkEyXkFqcGdeQXVyODY0NzcxNw@@._V1_SY1000_CR0,0,674,1000_AL_.jpg",
"Batman: Under the Red Hood":"https://m.media-amazon.com/images/M/MV5BYTdlODI0YTYtNjk5ZS00YzZjLTllZjktYmYzNWM4NmI5MmMxXkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
"Batman":"https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_.jpg",
"Batman Unmasked: The Psychology of the Dark Knight":"https://m.media-amazon.com/images/M/MV5BNjVlMjczMGItNTM5Ny00ZjFlLThjNTctYjIxN2IwMzQzMGY5XkEyXkFqcGdeQXVyNjU0NzE1NDY@._V1_SY1000_CR0,0,730,1000_AL_.jpg",
"Batman Beyond: Return of the Joker":"https://m.media-amazon.com/images/M/MV5BNmRmODEwNzctYzU1MS00ZDQ1LWI2NWMtZWFkNTQwNDg1ZDFiXkEyXkFqcGdeQXVyNTI4MjkwNjA@._V1_.jpg",
"Batman: Year One":"https://m.media-amazon.com/images/M/MV5BNTJjMmVkZjctNjNjMS00ZmI2LTlmYWEtOWNiYmQxYjY0YWVhXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SY1000_CR0,0,680,1000_AL_.jpg",
"Inception":"https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SY1000_CR0,0,675,1000_AL_.jpg",
"Interstellar":"https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_SX675_AL_.jpg",
"Out of the Furnace":"https://m.media-amazon.com/images/M/MV5BMTc2MTQ4MDU4NV5BMl5BanBnXkFtZTgwOTU1ODgzMDE@._V1_SY1000_CR0,0,664,1000_AL_.jpg",
"Batman Begins":"https://m.media-amazon.com/images/M/MV5BZmUwNGU2ZmItMmRiNC00MjhlLTg5YWUtODMyNzkxODYzMmZlXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SY1000_SX750_AL_.jpg",
"Doodlebug":"https://m.media-amazon.com/images/M/MV5BZTM0Nzk4ZDgtNWU1MC00ZDM0LTk2NTMtYWJmMDAyNDc1MTViXkEyXkFqcGdeQXVyNDQ2MTMzODA@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
"Memento":"https://m.media-amazon.com/images/M/MV5BZTcyNjk1MjgtOWI3Mi00YzQwLWI5MTktMzY4ZmI2NDAyNzYzXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,681,1000_AL_.jpg",
"Rare Birds":"https://m.media-amazon.com/images/M/MV5BMTkzNjIzNDM0OV5BMl5BanBnXkFtZTcwNzU3NDEzMQ@@._V1_.jpg",
"Carmen Miranda: Bananas Is My Business":"https://m.media-amazon.com/images/M/MV5BMTM4ODQyMzM5MV5BMl5BanBnXkFtZTcwNDYzMjYxMQ@@._V1_.jpg",
"The Fourth Protocol":"https://m.media-amazon.com/images/M/MV5BMjBlNzMyYzItNjM1Yy00N2ExLTg5MjItYzZkMjE0ZDA4ZDI1XkEyXkFqcGdeQXVyMTA0MjU0Ng@@._V1_SY1000_CR0,0,674,1000_AL_.jpg",
"Charade":"https://m.media-amazon.com/images/M/MV5BMzA5NWZjYTItNThmMC00YzM4LWExMzktZDlmYmIyYzNhMDI4XkEyXkFqcGdeQXVyNjUwMzI2NzU@._V1_SY1000_CR0,0,687,1000_AL_.jpg",
"Gone Fishin'":"https://m.media-amazon.com/images/M/MV5BZmFlMWMwYmUtMGEwNS00ZWVlLTlkNjctYTQ4NWUxMTIxOTg5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
"The Band Wagon":"https://m.media-amazon.com/images/M/MV5BNGUxZmJkZTgtMmI1Ny00Mzg3LWFlY2QtMjNkM2QwZGVhYTQyL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SY1000_CR0,0,663,1000_AL_.jpg",
"L.A. Story":"https://m.media-amazon.com/images/M/MV5BMjcwZGM4ODMtMjY1Yi00NTgwLTkxOWYtYWNiY2FkNjQ0MTlkXkEyXkFqcGdeQXVyNjE5MjUyOTM@._V1_.jpg",
"Meet Me in St. Louis":"https://m.media-amazon.com/images/M/MV5BZWVmZmRlNWQtYzYyMy00ZDljLWE5MjgtNDE5MGVmYTQ5NDk0XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SY1000_SX661_AL_.jpg",
"L'Enfer":"https://m.media-amazon.com/images/M/MV5BNDg0ZmE1MGMtM2I4Ny00OTk2LWFiMmMtNDRmYTIwMWE3OTI0XkEyXkFqcGdeQXVyMjQzMzQzODY@._V1_.jpg",
"Star Trek: Insurrection":"https://m.media-amazon.com/images/M/MV5BNWEzZDI0NjEtY2FkMC00ZjQwLWI2YzgtZDEyMzMwZmRlZDlhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_CR0,0,669,1000_AL_.jpg",
"Serial Mom":"https://m.media-amazon.com/images/M/MV5BYjM0N2ViMzUtMTc1OS00YmEzLWE2NWYtNjU5NTY4NjRlOTI0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_CR0,0,670,1000_AL_.jpg",
"Love and a .45":"https://m.media-amazon.com/images/M/MV5BMzI2MzUxOTcxM15BMl5BanBnXkFtZTcwMjQ2MDA4Mg@@._V1_.jpg",
"A Hungarian Fairy Tale":"https://m.media-amazon.com/images/M/MV5BMTQ0NjE0Nzg3NF5BMl5BanBnXkFtZTcwMjA4MzkxMQ@@._V1_.jpg",
"Before and After":"https://m.media-amazon.com/images/M/MV5BMTgwODk4NDkzNF5BMl5BanBnXkFtZTcwMjA0MjUyMQ@@._V1_.jpg",
"The Raven":"https://m.media-amazon.com/images/M/MV5BNTU4OGY5MjYtNTg5Zi00NGEyLTlhYTgtMTU3NzBmYmMzYWU4L2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SY1000_CR0,0,692,1000_AL_.jpg",
"Seconds":"https://m.media-amazon.com/images/M/MV5BZWQ3M2E4ODAtYzAzNi00MDU2LTliYWMtMTNiM2Y1MjNlZDY1XkEyXkFqcGdeQXVyMjkxNzQ1NDI@._V1_.jpg",
"Sleepless in Seattle":"https://m.media-amazon.com/images/M/MV5BNWY1MDJkZGUtZTE2OS00ODZiLTlmNzQtMDZjNzM2ZjkwM2QxXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_CR0,0,676,1000_AL_.jpg",
"Human Highway":"https://m.media-amazon.com/images/M/MV5BMTU3NDU1MDg3OF5BMl5BanBnXkFtZTYwOTYyODY5._V1_.jpg",
"Heartburn":"https://m.media-amazon.com/images/M/MV5BY2I3ODU4MWItZDJmOS00NGFkLTkzYWMtMWI4NTFmNDI2MjNmXkEyXkFqcGdeQXVyMTA0MjU0Ng@@._V1_.jpg",
"Sherlock Holmes and the Leading Lady":"https://m.media-amazon.com/images/M/MV5BN2Y0NDY2MzgtZmVlOC00ODdjLTlhMWUtYzE1MDUzYjg2OTEwXkEyXkFqcGdeQXVyMTk0MjQ3Nzk@._V1_.jpg"}



@app.route('/')
def mainPage():
    return render_template("mainPage.html")

@app.route("/user/<string:usermovie>")
def userRecommendation(usermovie):
    userMovie = usermovie.split("+")
    moviename = userMovie[1]
    userid = userMovie[0]
    base = userMovie[2]

    if userid in userDict:
        personalizedMovies = userDict[userid]
    else:
        personalizedMovies = userDict['1']
    similarMovies = userDict[base]
    personalizedPics = []
    similarPics = []
    for movie in personalizedMovies:
        personalizedPics.append(picDict[movie])
    for movie in similarMovies:
        similarPics.append(picDict[movie])

 
    return render_template('personalized.html', **locals())


if __name__ == "__main__":
    app.run()




















