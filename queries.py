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
def modify_value_of_data(cursor, table, attribute, PK, ID, amount):
    ''' 
    table: database table name
    attribute: attribute name (key in the dict) to modify
    PK: name of the Primary key field
    ID: primary key of the given entity to find
    amount: amount to change
    '''
    cursor.execute("SELECT " + attribute + " FROM " + table + " WHERE " + PK + " = " + ID + ";")
    result = cursor.fetchall()
    new_value = result[0][attribute] + amount
    cursor.execute("UPDATE " + table + " SET " + attribute + " = " + str(new_value) + " WHERE " + PK + " = " + ID + ";")


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


def get_value_of_an_attribute(cursor, table, attribute, PK, ID):
    cursor.execute("SELECT " + attribute + " FROM " + table + " WHERE " + PK + " = " + ID + ";")    
    result = cursor.fetchall()
    value = result[0][attribute]
    return value
