from flask import Flask, render_template, redirect, request, session
import datetime
from datetime import timezone
from operator import itemgetter
import queries
app = Flask(__name__)


@app.route("/all")
def route_list_all():
    questions = queries.get_questions_for_index()
    return render_template("list.html", questions=questions)


@app.route("/")
def route_list():
    questions = queries.get_latest_five_questions()
    return render_template("list.html", questions=questions)


@app.route("/getsearch", methods=['POST'])
def route_get_search():
    questions = queries.get_search_results(request.form["searchbox"])
    return render_template("list.html", questions=questions)


@app.route("/<aspect>=<desc>")
def route_list_aspect(aspect, desc):
    questions = queries.get_questions_for_index_ordered(aspect, desc)
    return render_template("list.html", questions=questions)


@app.route("/question/<int:id_>", methods=['GET'])
def route_question(id_):
    question = queries.get_question_by_id(id_)
    answers = queries.get_answers_by_question_id(id_)
    question_comments = queries.get_question_comments_by_question_id(id_,"question_id")
    answer_comments = queries.get_all_answer_comments()
    print(question)
    return render_template("question.html", question=question, answers=answers, questioncomments = question_comments, answercomments = answer_comments, id_=str(id_))


@app.route("/ask-question")
def route_ask():
    return render_template("form.html", page_title="Ask a question", action_link="/add-question")


@app.route("/question+1view/<int:ID>", methods=["GET"])
def route_question_view(ID):
    queries.modify_value_of_data("question", "view_number", "id", str(ID), 1)
    return redirect("/question/"+str(ID))


@app.route("/answer/<int:ID>/delete", methods=["GET"])
def route_answer_delete(ID):
    QID = queries.delete_answer_by_id(str(ID))
    return redirect("/question/"+str(QID))


@app.route("/question/<int:ID>/delete", methods=["GET"])
def route_question_delete(ID):
    queries.delete_question_and_answer_by_id(ID)
    return redirect("/")


@app.route("/question/<int:id_>/edit", methods=['GET'])
def route_question_edit(id_):
    question = queries.get_question_by_id(id_)
    return render_template(
        "form.html",
        page_title="Edit a question",
        action_link="/question/"+str(id_)+"/save",
        title_of_question=question[0]["title"],
        question=question[0]["message"])
    

@app.route("/question/<int:id_>/save", methods=['POST'])
def route_question_save(id_):
    queries.update_question_by_id(request.form["title"], request.form["question"], id_)
    return redirect("/question/" + str(id_))


@app.route("/give-answer/<int:ID>", methods=["POST"])
def route_add_answer(ID):
    list_to_write = [0,ID,request.form["answer_text"]]
    queries.add_answer(list_to_write)
    return redirect("/question/"+str(ID))


@app.route("/add-question", methods=["POST"])
def route_add():
    list_to_write = [0,0,request.form["title"], request.form["question"]]
    queries.add_question(list_to_write)
    return redirect("/")


@app.route("/give_comment/<table>/<int:id_>", methods=['POST'])
def route_give_comment(table,id_):
    comment_to_write = request.form["comment"]
    queries.add_comment(table, id_, comment_to_write)
    return redirect("/")


@app.route("/question/<int:ID>/vote-up", methods=['GET'])
def route_question_vote_up(ID):
    queries.modify_value_of_data("question", "vote_number", "id", str(ID), 1)
    return redirect("/question/"+str(ID))


@app.route("/question/<int:ID>/vote-down", methods=['GET'])
def route_question_vote_down(ID):
    queries.modify_value_of_data("question", "vote_number", "id", str(ID), -1)
    return redirect("/question/"+str(ID))


@app.route("/answer/<int:ID>/vote-up", methods=['GET'])
def route_answer_vote_up(ID):
    queries.modify_value_of_data("answer", "vote_number", "id", str(ID), 1)
    question_id = queries.get_value_of_an_attribute("answer", "question_id", "id", str(ID))
    return redirect("/question/"+str(question_id))


@app.route("/answer/<int:ID>/vote-down", methods=['GET'])
def route_answer_vote_down(ID):
    queries.modify_value_of_data("answer", "vote_number", "id", str(ID), -1)
    question_id = queries.get_value_of_an_attribute("answer", "question_id", "id", str(ID))
    return redirect("/question/"+str(question_id))
    

if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
