import database_common


@database_common.connection_handler
def get_questions_for_index(cursor):
    cursor.execute("SELECT * FROM question")
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_questions_for_index_ordered(cursor, aspect, desc):
    cursor.execute("SELECT * FROM question ORDER BY {} {}".format(aspect, desc))
    questions = cursor.fetchall()
    return questions




