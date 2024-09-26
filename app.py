from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/select', methods=['GET', 'POST'])
def select_survey():
     if request.method == 'POST':
          selected_survey = request.form.get("surveys")
          session["surveys_code"] = selected_survey
          session["responses"] = []
          return redirect(url_for("home_page"))
     

     return render_template("select.html", surveys=surveys)


@app.route("/", methods=["GET", "POST"])
def home_page():
        survey_code = session.get("survey_code")
        if not survey_code:
             return redirect(url_for("select_survey"))
        
        selected_survey = surveys[survey_code]

        if request.method == "POST":
            session["responses"] = []
            return redirect(url_for("show_qid", qid=0))
        

        return render_template("home.html", survey=selected_survey)


@app.route("/questions/<int:qid>", methods=['GET'])
def show_qid(qid):

    survey_code = session.get("survey_code")
    selected_survey = surveys[survey_code]


    responses = session.get("responses", [])

    if len(responses) == len(selected_survey.questions):
        return redirect(url_for("show_complete"))
    
    if qid != len(responses):
        flash("You are trying to access invalide question please procced in order")
        return redirect(url_for("show_qid", qid=len(responses)))


    if qid < 0 or qid >= len(selected_survey.questions):
        flash("Invalide access attempt")
        return "Question not found", 400
    
    question = selected_survey.questions[qid]
    return render_template("question.html", question=question, qid=qid, survey=selected_survey)


@app.route('/answer',  methods=['POST'])
def show_question():
    answer = request.form.get('answer')
    survey_code = session.get("survey_code")
    selected_survey = surveys[survey_code]
    responses = session.get("responses", [])
    current_question = selected_survey.questions[len(session["responses"])]

    if not current_question.validate_answer(answer):
         flash("Invalide answer, please try again!")
         return redirect(url_for("show_qid", qid=len(session["responses"])))


    responses.append(answer)
    session["responses"] = responses


    if len(responses) == len(selected_survey.questions):
         return redirect(url_for("show_complete"))
    else:
         return redirect(url_for("show_qid", qid=len(responses)))
    

@app.route('/complete')
def show_complete():
    responses = session.get("responses", [])
    return render_template("complete.html", responses=responses)


@app.route('/reset', methods=['POST'])
def reset_survey():
     session["responses"] = []
     flash("The survey has been reset, try again please if you would like to fill survey out!")
     return redirect(url_for("home_page"))