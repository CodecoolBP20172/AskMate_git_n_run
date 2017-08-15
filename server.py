from flask import Flask, render_template, redirect, request, session
import csv
import datetime
import base64


app = Flask(__name__)


def string_to_base64(origin):
    origin_in_bytes = origin.encode('utf-8')
    b64_encoded_bytes = base64.b64encode(origin_in_bytes)
    return b64_encoded_bytes.decode('utf-8')


def base64_to_string(encoded_string):
    decoded_string = base64.b64decode(encoded_string)
    return decoded_string.decode('utf-8')


def read_file(csvfile):
    data = []
    with open(csvfile, "r") as datafile:
        file = csv.reader(datafile, delimiter=",")
        for row in file:
            data.append(row)
    return data


def write_file(question):
    with open("question.csv", "a") as datafile:
        file = csv.writer(datafile, delimiter=",")
        file.writerow(question)

def write_to_file(csvfile, data):
    with open(csvfile, "w") as datafile:
        file = csv.writer(datafile, delimiter=",")
        for line in data:
            file.writerow(line)

def voting(csvfile, ID, vote_index, amount):
    list_from_file = read_file(csvfile)
    for line in list_from_file:
        if ID == line[0]:
            line[vote_index] += amount
    write_to_file(csvfile, list_from_file)


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
    return render_template("question.html", questions=read_file("question.csv"), id_=str(ID))


@app.route("/ask-question")
def route_ask():
    return render_template("form.html")


@app.route("/add-question", methods=["POST"])
def route_add():
    list_to_write = [3,int(datetime.datetime.utcnow().timestamp()),0,0,string_to_base64(request.form["title"]), string_to_base64(request.form["question"])]
    write_file(list_to_write)
    return redirect("/")

@app.route("/question/<int:ID>/vote-up", methods=['GET'])
def route_question_vote_up(ID):
    voting("question.csv", ID, 3, 1)
    return redirect("/question/"+str(ID))

@app.route("/question/<int:ID>/vote-down", methods=['GET'])
def route_question_vote_down(ID):
    voting("question.csv", ID, 3, -1)
    return redirect("/question/"+str(ID))

@app.route("/answer/<int:ID>/vote-up", methods=['GET'])
def route_answer_vote_up(ID):
    voting("answer.csv", ID, 2, 1)
    return redirect("/answer/"+str(ID))

@app.route("/answer/<int:ID>/vote-down", methods=['GET'])
def route_answer_vote_down(ID):
    voting("answer.csv", ID, 2, -1)
    return redirect("/answer/"+str(ID))


if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
