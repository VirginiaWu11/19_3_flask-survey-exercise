from flask import Flask, request, render_template, redirect, flash, jsonify, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route('/')
def show_form():
    return render_template('home.html', survey = satisfaction_survey)

@app.route('/flask-session', methods = ['POST'])
def handle_session():
    session["responses"] = []
    return redirect('questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session["responses"]
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
    responses = session['responses'] 
    responses.append(answer)
    session["responses"] = responses

    if len(responses) >= len(satisfaction_survey.questions):       
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank-you')
def show_thankyou():
    print('$*#**%***********************')
    print(session, session['responses'])
    return render_template('thank-you.html')