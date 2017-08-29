import database_common


@database_common.connection_handler
def get_questions_for_index(cursor):
    cursor.execute("SELECT * FROM question")
    questions = cursor.fetchall()
    print(questions)
    return questions



