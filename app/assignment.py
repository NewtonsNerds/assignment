import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from datetime import datetime
from contextlib import closing
		
# configuration variables
DATABASE = '.\\db\\log.db' #note this is setup for windows
DEBUG = True
SECRET_KEY = 'TooManySecrets'
USERNAME = 'user'
PASSWORD = 'password'

# create app object
app = Flask(__name__)
app.config.from_object(__name__)

# connect to database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Initialise database
# Source: http://flask.pocoo.org/docs/0.10/tutorial/dbinit/#tutorial-dbinit
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Decorator executes before request 
# From http://flask.pocoo.org/docs/0.10/tutorial/dbcon/#tutorial-dbcon
@app.before_request
def before_request():
	# g is a special function level object that only stores information for a single request 
    g.db = connect_db()

# Decorator executes after reponse has been constructed 
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    FMT = '%H:%M'

    cur = g.db.execute('select user, log, start_time, end_time from entries order by id desc')
    entries = [dict(
        user=row[0],
        log=row[1], 
        start_time=row[2], 
        end_time=row[3], 
        time=(datetime.strptime(row[3], FMT)-datetime.strptime(row[2], FMT))) 
    for row in cur.fetchall()]

    ttime = datetime.strptime('00:00', FMT)
    for entry in entries:
        ttime = (ttime + entry['time'])

    totaltime = ttime.time().strftime(FMT)
    
    return render_template('show_entries.html', entries=entries, username=USERNAME, totaltime=totaltime)


@app.route('/add_entry', methods=['POST'])
def add_entry():
    validated = True
    if not validated:
        abort(401)
    g.db.execute('insert into entries (user, log, start_time, end_time) values (?, ?, ?, ?)',
                 [request.form['user'], request.form['log'], request.form['start_time'], request.form['end_time']])
    g.db.commit()
    flash('New log entry was successfully saved.')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
            flash('Sorry, there is no matching username.')
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            flash('Computer says no, your password is wrong.')
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()