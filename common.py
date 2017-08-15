import csv
import datetime
import base64


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