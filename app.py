from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    """
        populate home page with info from survey
        begin survey
    """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/questions/<int:ques_num>')
def ask_questions(ques_num):
    """
        make sure user is on correct page
        ask question and submit answer
    """
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/thank_you")

    if (len(responses) != ques_num):
        flash("Invalid question page")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[ques_num]
    return render_template("questions.html", question_num=ques_num, question=question)

@app.route('/answer', methods=['POST'])
def add_answer():
    """
        add answer to response list and move on to next question
    """

    answer = request.form['answer']
    responses.append(answer)
    
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/thank_you")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/thank_you')
def thank_you_page():
    return render_template("thank_you.html")
