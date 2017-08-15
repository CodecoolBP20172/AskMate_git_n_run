from flask import Flask, render_template, redirect, request, session
import csv

server_object = Flask(__name__)

def read_file(csvfile):
    data = []
    with open(csvfile, "r") as datafile:
        file = csv.reader(datafile, delimiter=",")
        for row in file:
            data.append(row)
    return data


@server_object.route("/")
def route_list():
    return render_template("list.html", questions=read_file("question.csv"))


if __name__ == "__main__":
    server_object.secret_key = "server_object_magic"  # Change the content of this string
    server_object.run(
        debug=True,
        port=5000
    )

'''
a = [1, 2, 3, 4, 5, "fuck this shit", 7]
    

def write_file(abrakadabra):
    with open("question.csv", "a") as datafile:
        file = csv.writer(datafile, delimiter=",")
        file.writerow(abrakadabra)
'''        