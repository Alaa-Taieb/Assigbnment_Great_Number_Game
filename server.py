from flask import Flask, render_template, redirect, session, request
import random
app = Flask(__name__)
app.secret_key = "Hash won't fail me"

@app.route('/')
def guess():
    if 'tries' not in session:
        session['tries'] = 0
    if 'number' not in session:
        session['number'] = random.randint(1,100)
    if 'feedback' not in session:
        session['feedback'] = "none"
    
    return render_template("index.html", number = session['number'], feedback = session['feedback'], tries = session['tries'])

@app.route('/check', methods = ['post'])
def check():
    if 'tries' not in session:
        session['tries'] = 0
    session['tries'] += 1
    user_input = int(request.form['answer'])
    number = session['number']
    if user_input == number:
        session['feedback'] = 'correct'
    elif user_input > number:
        session['feedback'] = 'too high'
    else:
        session['feedback'] = 'too low'
    return redirect('/')

@app.route('/reset')
def reset():
    session.pop('number')
    session.pop('feedback')
    session.pop('tries')
    return redirect('/')

@app.route('/submit_score' , methods = ['post'])
def submit_score():
    if 'scores_table' not in session:
        session['scores_table'] = []
    name = request.form['name']
    obj = {'name': name, 'tries': session['tries']}
    leaderboard = session['scores_table']
    session.clear()
    leaderboard.append(obj)
    session['scores_table'] = leaderboard
    return redirect('/leaderboard')

@app.route('/leaderboard')
def leaderboard():
    scores = session['scores_table']
    return render_template('leaderboard.html' , scores = scores)

if __name__ == "__main__":
    app.run(debug = True)