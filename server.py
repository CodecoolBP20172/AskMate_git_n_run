from flask import Flask, render_template, redirect, request, session
import csv
import datetime

app = Flask(__name__)

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

@app.route("/")
def route_list():
    questions = read_file("question.csv")
    for number, line in enumerate(questions):
        questions[number][1] = datetime.datetime.utcfromtimestamp(float(line[1]))
        print(questions[number][1])
    return render_template("list.html", questions=questions)

@app.route("/ask-question")
def route_ask():
    return render_template("form.html")


@app.route("/add-question", methods=["POST"])
def route_add():
    list_to_write = [3,int(datetime.datetime.utcnow().timestamp()),0,0,request.form["title"], request.form["question"]]
    write_file(list_to_write)
    return redirect("/")



    '''
    for x in range() < len(list_of_keys) - 1:
                content_to_save += request.form[list_of_keys[i]] + ";"
                i += 1
            content_to_save += request.form[list_of_keys[i]]
    '''

    return redirect("/")

if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
