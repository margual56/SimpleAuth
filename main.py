import atexit
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from Database import DatabaseWrapper
import os
import sys

app = Flask(__name__, static_folder="static")
db = None


@app.route('/')
def home():
    if session.get('logged_in'):
        return render_template('controlpanel.html')
    else:
        return redirect("/login")


@app.route('/login', methods=['POST', 'GET'])
def login(incorrect=False):
    if request.method == 'POST':
        correct = db.checkUser(request.form['username'], request.form['password'])

        if correct:
            session['logged_in'] = True
            return redirect(url_for('home'))

        return render_template('login.html', incorrect=True)
    else:
        if session.get('logged_in'):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', incorrect=False)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/newaccount", methods=['POST', 'GET'])
def newuser():
    if request.method == "POST":
        if request.form['password1'] == request.form['password2']:
            if db.userExists(request.form['username']):
                flash("User exists")
                return redirect(url_for('login'))

            db.newUser(request.form['username'], request.form['password1'])

            return redirect(url_for('login'))
        else:
            flash("User exists")
            return redirect(url_for('newuser'))
    else:
        return render_template('newuser.html')


# @app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


if __name__ == '__main__':
    production = False

    if len(sys.argv) == 2:
        production = bool(sys.argv[1])

    password = input('Password for the database: ')

    db = DatabaseWrapper('admin_web', password)
    atexit.register(db.close)  # On clean exit, close the connections

    app.secret_key = os.urandom(12)

    app.run(host="localhost", port=80)  # Use for testing