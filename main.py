# Create an application
from flask import Flask, url_for, request, render_template
app = Flask(__name__)

@app.route("/")
def show_all_songs():
    return render_template('songs.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))
    #Chap. 3.3 test for user logged in failed, so redirect to login url

@app.route('/search', methods=["GET", "POST"])
def search():
    return render_template('songs.html', songs=songs)

@app.route('/artist', methods=["GET", "POST"])
def artist():
    return render_template('songs.html', songs=songs)

@app.route('/genre', methods=["GET", "POST"])
def genre():
    return render_template('songs.html', songs=songs)


@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the requested page - 404"

if __name__ == "__main__"
    app.run(host='0.0.0.0', debug=True)
