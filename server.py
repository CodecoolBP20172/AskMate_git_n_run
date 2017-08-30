from flask import Flask, render_template, redirect, request, session
import datetime
from datetime import timezone
from operator import itemgetter
import queries
app = Flask(__name__)


@app.route("/")
def route_list():
    questions = queries.get_questions_for_index()
    return render_template("list.html", questions=questions)


@app.route("/<aspect>=<desc>")
def route_list_aspect(aspect, desc):
    questions = queries.get_questions_for_index_ordered(aspect, desc)
    return render_template("list.html", questions=questions)


@app.route("/question/<int:id_>", methods=['GET'])
def route_question(id_):
    question = queries.get_question_by_id(id_)
    answers = queries.get_answers_by_question_id(id_)
    return render_template("question.html", question=question, answers=answers, id_=str(id_))


@app.route("/ask-question")
def route_ask():
    return render_template("form.html", page_title="Ask a question", action_link="/add-question")


@app.route("/question+1view/<int:ID>", methods=["GET"])
def route_question_view(ID):
    queries.modify_value_of_data("question", "view_number", "id", str(ID), 1)
    return redirect("/question/"+str(ID))


@app.route("/answer/<int:ID>/delete", methods=["GET"])
def route_answer_delete(ID):
    answer_table = read_file("answer.csv")
    for line in answer_table:
        if line[0] == str(ID):
            kutya = line[3]
    for line in answer_table:
        if int(line[0]) == ID:
            answer_table.remove(line)
    write_to_file("answer.csv", answer_table)
    return redirect("/question/"+str(kutya))


@app.route("/question/<int:ID>/delete", methods=["GET"])
def route_question_delete(ID):
    answer_table = read_file("answer.csv")
    answers_to_remove = []
    for line in answer_table:
        if int(line[3]) == ID:
            answers_to_remove.append(line)
    for line in answers_to_remove:
        answer_table.remove(line)
    write_to_file("answer.csv", answer_table)
    questions_table = read_file("question.csv")
    for line in questions_table:
        if int(line[0]) == ID:
            questions_table.remove(line)
    write_to_file("question.csv", questions_table)
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
    list_to_write = [nextID("answer.csv"), int(datetime.datetime.now().timestamp()),0,ID,string_to_base64(request.form["answer_text"]), ""]
    write_file("answer.csv", list_to_write)
    return redirect("/question/"+str(ID))


@app.route("/add-question", methods=["POST"])
def route_add():
    list_to_write = [nextID("question.csv"),int(datetime.datetime.now().timestamp()),0,0,string_to_base64(request.form["title"]), string_to_base64(request.form["question"])]
    write_file("question.csv", list_to_write)
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


@app.route("/search/<searchkey>", methods=['GET'])
def route_answer_search(searchkey):
    questions = queries.get_search_results(searchkey)
    return render_template("list.html", questions=questions)
    

if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
