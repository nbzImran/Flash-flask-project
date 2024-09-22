from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)


@app.route("/", methods=["GET", "POST"])
def home_page():
        if request.method == "POST":
            session["responses"] = []
            return redirect(url_for("show_qid", qid=0))
        

        return render_template("home.html", survey=satisfaction_survey)


@app.route("/questions/<int:qid>", methods=['GET'])
def show_qid(qid):


    responses = session.get("responses", [])

    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for("show_complete"))
    
    if qid != len(responses):
        flash("You are trying to access invalide question please procced in order")
        return redirect(url_for("show_qid", qid=len(responses)))


    if qid < 0 or qid >= len(satisfaction_survey.questions):
        flash("Invalide access attempt")
        return "Question not found", 400
    
    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question=question, qid=qid, survey=satisfaction_survey)


@app.route('/answer',  methods=['POST'])
def show_question():
    answer = request.form.get('answer')
    responses = session.get("responses", [])


    responses.append(answer)
    session["responses"] = responses

    if len(responses) == len(satisfaction_survey.questions):
         return redirect(url_for("show_complete"))
    else:
         return redirect(url_for("show_qid", qid=len(responses)))
    

@app.route('/complete')
def show_complete():
    return f"""Thank you for completing the survey your resposes will be confidential, here are your answers: {session["responses"]}"""