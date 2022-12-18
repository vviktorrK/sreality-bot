import psycopg2
import psycopg2.extras
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def show_flats():
    conn = psycopg2.connect(host='postgres_db', user='postgres', password='password', database='sreality_bot')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM apartments')
    apartments = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', apartments=apartments)
