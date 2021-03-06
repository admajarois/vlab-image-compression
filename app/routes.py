from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():

    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Hello', greeting=greeting)