from flask import Flask, render_template, redirect, request, session
import csv
import datetime
import base64
from common import *


app = Flask(__name__)


@app.route("/")
def route_list():
    questions = read_file("question.csv")
    for number, line in enumerate(questions):
        questions[number][1] = datetime.datetime.utcfromtimestamp(float(line[1]))
        questions[number][4] = base64_to_string(line[4])
        questions[number][5] = base64_to_string(line[5])
    return render_template("list.html", questions=questions)


@app.route("/question/<int:ID>", methods=['GET'])
def route_question(ID):
    questions = read_file("question.csv")
    answers = read_file("answer.csv")
    modify_value_of_data("question.csv", ID, 2, 1)
    for number, line in enumerate(questions):
        questions[number][4] = base64_to_string(line[4])
        questions[number][5] = base64_to_string(line[5])
    for number, line in enumerate(answers):
        answers[number][4] = base64_to_string(line[4])
        answers[number][5] = base64_to_string(line[5])
    return render_template("question.html", questions=questions, answers=answers, id_=str(ID))


@app.route("/ask-question")
def route_ask():
    return render_template("form.html")




@app.route("/add-question", methods=["POST"])
def route_add():
    list_to_write = [nextID("question.csv"),int(datetime.datetime.utcnow().timestamp()),0,0,string_to_base64(request.form["title"]), string_to_base64(request.form["question"])]
    write_file(list_to_write)
    return redirect("/")

@app.route("/question/<int:ID>/vote-up", methods=['GET'])
def route_question_vote_up(ID):
    print("asd")
    modify_value_of_data("question.csv", ID, 3, 1)
    return redirect("/question/"+str(ID))

@app.route("/question/<int:ID>/vote-down", methods=['GET'])
def route_question_vote_down(ID):
    modify_value_of_data("question.csv", ID, 3, -1)
    return redirect("/question/"+str(ID))

@app.route("/answer/<int:ID>/vote-up", methods=['GET'])
def route_answer_vote_up(ID):
    modify_value_of_data("answer.csv", ID, 2, 1)
    return redirect("/answer/"+str(ID))

@app.route("/answer/<int:ID>/vote-down", methods=['GET'])
def route_answer_vote_down(ID):
    modify_value_of_data("answer.csv", ID, 2, -1)
    return redirect("/answer/"+str(ID))

'''
Sort questions:
The list of questions should be sortable according to: date, votes, number of views 
(both in ascending and descending order) (/list?time=asc;title=desc,...)
'''


if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
