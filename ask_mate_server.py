from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)


def open_file():
    data = []
    with open("question.csv", "r") as datafile:
        file = csv.reader(datafile, delimiter=",")
        for row in file:
            data.append(row)
    return data

if __name__ == "__main__":
    app.secret_key = "123"
    app.run(
        debug=True,
        port=5000
        )
