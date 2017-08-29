from flask import Flask, render_template, redirect, request, session
import csv
import datetime
from datetime import timezone
import base64
from common import *
from operator import itemgetter
import queries

app = Flask(__name__)


@app.route("/")
def route_list():
    questions = queries.get_questions_for_index()
    return render_template("list.html", questions=questions)


@app.route("/<aspect>=<desc>")
def route_list_aspect(aspect, desc):
    questions = read_file("question.csv")
    for line_number, line in enumerate(questions):
        questions[line_number][1] = datetime.datetime.fromtimestamp(float(line[1]))
        questions[line_number][4] = base64_to_string(line[4])
        questions[line_number][5] = base64_to_string(line[5])
        questions[line_number][2] = int(line[2])
    dictionary_of_orders = {"name": 4, "date": 1, "view": 2, "vote": 3}
    aspect_number = 0
    if aspect in dictionary_of_orders:
        aspect_number = dictionary_of_orders[aspect]
    questions = sorted(questions, key=itemgetter(aspect_number))
    if desc == "desc":
        questions = reversed(questions) 
    return render_template("list.html", questions=questions)


@app.route("/question/<int:ID>", methods=['GET'])
def route_question(ID):
    questions = read_file("question.csv")
    answers = read_file("answer.csv")
    for line_number, line in enumerate(questions):   
        questions[line_number][1] = datetime.datetime.fromtimestamp(float(line[1]))
        questions[line_number][4] = base64_to_string(line[4])
        questions[line_number][5] = base64_to_string(line[5])
    for line_number, line in enumerate(answers):
        answers[line_number][1] = datetime.datetime.fromtimestamp(float(line[1]))
        answers[line_number][4] = base64_to_string(line[4])
        answers[line_number][5] = base64_to_string(line[5])
    answers = reversed(sorted(answers, key=itemgetter(2)))
    return render_template("question.html", questions=questions, answers=answers, id_=str(ID))


@app.route("/ask-question")
def route_ask():
    return render_template("form.html", page_title="Ask a question", action_link="/add-question")


@app.route("/question+1view/<int:ID>", methods=["GET"])
def route_question_view(ID):
    modify_value_of_data("question.csv", ID, 2, 1)
    print("asd")
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
    

@app.route("/question/<int:ID>/edit", methods=['GET'])
def route_question_edit(ID):
    list_from_csv = read_file("question.csv")
    list_of_data_to_edit = ""
    for line in list_from_csv:
        if str(ID) == line[0]:
            list_of_data_to_edit = line
    return render_template(
        "form.html",
        page_title="Edit a question",
        action_link="/question/"+str(ID)+"/save",
        title_of_question=base64_to_string(list_of_data_to_edit[4]),
        question=base64_to_string(list_of_data_to_edit[5]))


@app.route("/question/<int:ID>/save", methods=['POST'])
def route_question_save(ID):
    list_to_modify = read_file("question.csv")
    for line in list_to_modify:
        if str(ID) == line[0]:
            line[4] = string_to_base64(request.form["title"])
            line[5] = string_to_base64(request.form["question"])
    write_to_file("question.csv", list_to_modify)
    return redirect("/question/" + str(ID))


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
    modify_value_of_data("question.csv", ID, 3, 1)
    return redirect("/question/"+str(ID))


@app.route("/question/<int:ID>/vote-down", methods=['GET'])
def route_question_vote_down(ID):
    modify_value_of_data("question.csv", ID, 3, -1)
    return redirect("/question/"+str(ID))


@app.route("/answer/<int:ID>/vote-up", methods=['GET'])
def route_answer_vote_up(ID):
    modify_value_of_data("answer.csv", ID, 2, 1)
    answers = read_file("answer.csv")
    for line in answers:
        if line[0] == str(ID):
            kutya = line[3]
    return redirect("/question/"+str(kutya))


@app.route("/answer/<int:ID>/vote-down", methods=['GET'])
def route_answer_vote_down(ID):
    modify_value_of_data("answer.csv", ID, 2, -1)
    answers = read_file("answer.csv")
    for line in answers:
        if line[0] == str(ID):
            kutya = line[3]
    return redirect("/question/"+str(kutya))


if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
