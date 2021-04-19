from flask import Flask, request, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


responses = []

@app.route('/')
def show_form():
    return render_template('home.html', survey = satisfaction_survey)

@app.route('/questions/<int:qid>')
def show_question(qid):
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thank-you')
    elif qid != len(responses):
        flash("You're trying to access an invalid question. Here is the current question")        
        return redirect(f'/questions/{len(responses)}')
    else:    
        return render_template('question.html', question = satisfaction_survey.questions[qid], qid = qid)


@app.route('/answer', methods = ['POST'])
def add_res():
    answer = request.form['answer']
    responses.append(answer)
    if len(responses) >= len(satisfaction_survey.questions):
        
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank-you')
def show_thankyou():
    return render_template('thank-you.html')