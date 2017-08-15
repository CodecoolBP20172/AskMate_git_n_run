import csv


a = [1, 2, 3, 4, 5, "fuck this shit", 7]
    

def write_file(abrakadabra):
    with open("question.csv", "a") as datafile:
        file = csv.writer(datafile, delimiter=",")
        file.writerow(abrakadabra)


def read_file():
    data = []
    with open("question.csv", "r") as datafile:
        file = csv.reader(datafile, delimiter=",")
        for row in file:
            data.append(row)
    return data

write_file(a)
print(read_file())