import database_common


@database_common.connection_handler
def get_questions_for_index(cursor):
    cursor.execute("SELECT id, submission_time, view_number, vote_number, title FROM question")
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_questions_for_index_ordered(cursor, aspect, desc):
    cursor.execute("SELECT id, submission_time, view_number, vote_number, title FROM question ORDER BY {} {}".format(aspect, desc))
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_question_by_id(cursor, id_):
    cursor.execute("SELECT * FROM question WHERE id = {}".format(id_))
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answers_by_question_id(cursor, id_):
    cursor.execute("SELECT * FROM answer WHERE question_id = {}".format(id_))
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def update_question_by_id(cursor, title, msg, id_):
    cursor.execute("UPDATE question SET title=%s, message=%s WHERE id = {}".format(id_),(title, msg))