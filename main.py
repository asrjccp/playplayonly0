from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    conn = get_db_connection()
    selections = conn.execute('SELECT * FROM selections').fetchall()
    conn.close()
    common_topics = sum(1 for selection in selections if selection['student'] == selection['teacher'] == 1)
    return render_template('teacher.html', common_topics=common_topics)

@app.route('/submit', methods=['POST'])
def submit():
    selections = request.form
    conn = get_db_connection()
    conn.execute('DELETE FROM selections')
    conn.execute('INSERT INTO selections (topic1, topic2, topic3, topic4, topic5) VALUES (?, ?, ?, ?, ?)', (selections.get('topic1'), selections.get('topic2'), selections.get('topic3'), selections.get('topic4'), selections.get('topic5')))
    conn.commit()
    conn.close()
    return redirect(url_for('teacher'))

app.run(host='0.0.0.0', port=8080)
