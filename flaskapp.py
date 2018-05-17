from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import psycopg2
import movie
import re
app = Flask(__name__)
Bootstrap(app)


conn = psycopg2.connect("postgresql://garipa01:@knuth.luther.edu/movies")
cur = movies.cursor()
movieObj = movie.Movie()

def populate():
    cur.execute("SELECT DISTINCT LEFT(title,1) as letter from moviecast order by letter")
    res = cur.fetchall()
    charList = []
    cList = []
    for c in res:
        charList.append(c[0])
    charList.sort()
    for i in range(23,49):
        cList.append(charList[i])
    cList.append(' ')
    for i in range(0,10):
        cList.append(str(i))
    return cList


cList = populate()

@app.route('/')
def start():
    movieObj.reset()
    return render_template('index.html', charList = cList, mStr = movieObj.get())

@app.route('/getChar', methods=["POST"])
def getChar():
    char = request.form['char']
    movieObj.add(char)
    cur.execute("SELECT DISTINCT title from moviecast where upper(substr(title,1," + str(len(movieObj)) + ")) = upper('"+ movieObj.get() +"') ")
    res = cur.fetchall()
    movieList = []
    for mv in res:
        movieList.append(mv[0])
    movieList = sorted(movieList, key=str.lower)
    return render_template('index2.html', charList = cList,mStr = movieObj.get(), mlist = movieList)

@app.route('/removeChar',methods=["POST"])
def removeChar():
    if len(movieObj) != 0:
        movieObj.remove()
        cur.execute("SELECT DISTINCT title from moviecast where upper(substr(title,1," + str(len(movieObj)) + ")) = upper('"+ movieObj.get() +"') ")
        res = cur.fetchall()
        movieList = []
        for mv in res:
            movieList.append(mv[0])
        movieList = sorted(movieList, key=str.lower)
        return render_template('index2.html', charList = cList,mStr = movieObj.get(), mlist = movieList)
    else:
        movieObj.reset()
        return render_template('index.html', charList = cList, mStr = movieObj.get())

@app.route('/movie',methods=["POST"])
def moviePage():
    mv = request.form['mv']
    if not (bool(re.search('\d',mv))):
        cur.execute("SELECT * from moviecast where title = '"+ mv + "'")
        res = cur.fetchall()
        mlist = []
        for part in res:
            plist = []
            for i in range(len(part)):
                if (i+1) != len(part):
                    plist.append(part[i])
            mlist.append(plist)
        return render_template('movie.html',movie = mv, actors = mlist)
    else:
        return render_template('error.html')

@app.route('/restart',methods=["GET","POST"])
def restart():
    movieObj.reset()
    return render_template('index.html', charList = cList, mStr = movieObj.get())


if __name__ == "__main__":
    app.run(port=5001, debug=True)