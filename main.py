from sqlite3 import dbpi2 as sqlite3
from contextlib import closing

# Create an application
from flask import Flask, url_for, request, render_template, redirect, g,
session, flash

DATABASE = 'data/songs.db'
DEBUG = True #set debug=False before publishing
SECRET_KEY = 'abcd1234'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#all uppercase variables defined will be added to config

#connect to database
def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

def init_db():
    print("Initializing database")
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    print("Filling database")
    with closing(connect_db()) as db:
        file = open('testing/songs.example', 'r')
        for line in file:
            line = line.rstrip("\n")
            print(line.split("-"))
            title, artist, genre = line.split('-')
            db.execute("insert into songs (title, artist, genre) values
            (?,?,?)", [title,artist,genre])
        db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.before_request
def before_request():
    g.db = connect_db() 
#g: flask object for one request

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/")
def show_all_songs():
    if session.get("logged_in") == True:
        cur = g.db.execute('select title, artist, genre from songs oder by id
        desc')
        songs = [dict(title=row[0], artist=row[1], genre=row[2]) for now in
        cur.fetchall()]
        return render_template('songs.html', songs=songs)
    else:
        return render_template("login.html")

@app.route('/login')
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == app.config["USERNAME"] and \
           request.form["password"] == app.config["PASSWORD"]:
              session['login_in'] = True
              flash("You are now logged in as " + app.config["USERNAME"] + ".")
              return redirect(url_for("show_all_songs"))
        else:
            error = "Invalid user credentials!"
    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('login')
# Chap.3.3 test for user logged in failed, so redirect to login url

#simple search: only matches when the searchterm is exactly matched!
@app.route('/search', methods=["GET", "POST"])
def search():
    s = request.args["searchterm"]
    cur = g.db.execute("select title, artist, genre from songs where (title = ?
    or artist = ? or genre = ?)", [s,s,s])
    songs = [dict(title=row[0], artist=row[1], genre=row[2]) for row in
    cur.fetchall()]
    return render_template('songs.html', songs=songs)

@app.route('/artist', methods = ["GET","POST"]
def artist():
    artist = request.args["artist"]
    cur = g.db.execute("select title, artist, genre from songs where artist =
    ?", [artist])
    songs = [dict(title=row[0], artist=row[1], genre=row[2]) for row in
    cur.fetchall()]
    return render_template('songs.html', songs=songs)

@app.route('/genre', methods = ["GET","POST"]
def genre():
    genre = request.args["genre"]
    cur = g.db.execute("select title, artist, genre from songs where genre =
    ?", [genre])
    songs = [dict(title=row[0], artist=row[1], genre=row[2]) for row in
    cur.fetchall()]
    return render_template('songs.html', songs=songs)

@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the requested page - 404"

if __name__ == "__main__"
    app.run(host='0.0.0.0')

