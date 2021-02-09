'''
MIT License

Copyright (c) 2021 Marcos Gutiérrez Alonso and Silvia Rodríguez Bares

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

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
        return render_template('controlpanel.html', isAdmin=db.isAdmin(session.get('username')))
    else:
        return redirect("/login")


@app.route('/login', methods=['POST', 'GET'])
def login(incorrect=False):
    if request.method == 'POST':
        correct = db.checkUser(request.form['username'], request.form['password'])

        if correct:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect('/')

        return render_template('login.html', incorrect=True)
    else:
        if session.get('logged_in'):
            return home()
        else:
            return render_template('login.html', incorrect=incorrect)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
    return home()


@app.route("/newuser", methods=['POST', 'GET'])
def newuser():
    if request.method == "POST":
        if db.userExists(request.form['username']):
            flash("User exists")
            return redirect(url_for('login'))

        if bool(request.form.getlist('IsAdmin')):
            if not db.newUser(request.form['username'], request.form['password'], True, request.form['passwordadmin']):
                return render_template('newuser.html', incorrect=True)
        else:
            db.newUser(request.form['username'], request.form['password'])

        return redirect(url_for('login'))
    else:
        return render_template('newuser.html', incorrect=False)


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

    app.run(host="0.0.0.0", port=8000)  # Use for testing
