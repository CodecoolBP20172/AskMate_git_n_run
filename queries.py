import database_common
from datetime import datetime

dt = datetime.now()

# Get values------------------------------------------------------------------------------------------


@database_common.connection_handler
def get_questions_for_index(cursor):
    cursor.execute("SELECT id, submission_time, view_number, vote_number, title FROM question")
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_question_id_from_answer_id(cursor, answer_id):
    cursor.execute("SELECT question_id FROM answer WHERE id = {}".format(answer_id))
    actual_question_id = cursor.fetchall()
    return actual_question_id[0]["question_id"]


@database_common.connection_handler
def get_questions_for_index_ordered(cursor, aspect, desc):
    cursor.execute('''SELECT id, submission_time, view_number, vote_number, title
                      FROM question
                      ORDER BY {} {}'''.format(aspect, desc))
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_question_by_id(cursor, id_):
    cursor.execute("SELECT * FROM question WHERE id = {}".format(id_))
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answers_by_question_id(cursor, id_):
    cursor.execute("SELECT * FROM answer WHERE question_id = {} ORDER BY vote_number DESC".format(id_))
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_question_comments_by_question_id(cursor, id_, q_or_a):
    cursor.execute("SELECT * FROM comment WHERE {} = {}".format(q_or_a, id_))
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_all_answer_comments(cursor):
    cursor.execute("SELECT * FROM comment WHERE question_id IS NULL")
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_value_of_an_attribute(cursor, table, attribute, PK, ID):
    cursor.execute("SELECT " + attribute + " FROM " + table + " WHERE " + "PK" + " = " + ID + ";")
    result = cursor.fetchall()
    value = result[0][attribute]
    return value


@database_common.connection_handler
def get_search_results_in_answer(cursor, searchkey):
    cursor.execute("SELECT question_id FROM answer WHERE LOWER(message) LIKE '%{}%'".format(searchkey.lower()))
    ids_found_searchkey_in_answers = cursor.fetchall()
    return ids_found_searchkey_in_answers


@database_common.connection_handler
def get_search_results(cursor, searchkey):
    ids = []
    found_questions = []
    for line in get_search_results_in_answer(searchkey):
        ids.append(str(line["question_id"]))
    for line in get_search_results_in_questions(searchkey):
        ids.append(str(line["id"]))
    for ID in ids:
        cursor.execute("SELECT * FROM question WHERE id = {}".format(ID))
        question_to_append = cursor.fetchall()
        found_questions.append(question_to_append[0])
    return found_questions


@database_common.connection_handler
def get_latest_five_questions(cursor):
    cursor.execute('''SELECT id, submission_time, view_number, vote_number, title
                      FROM question
                      ORDER BY submission_time
                      LIMIT 5''')
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_search_results_in_questions(cursor, searchkey):
    cursor.execute('''SELECT id FROM question
                      WHERE LOWER(title) LIKE '%{}%'
                      or LOWER(message) LIKE '%{}%' '''.format(
                          searchkey.lower(),
                          searchkey.lower()))
    ids_found_searchkey_in_question = cursor.fetchall()
    return ids_found_searchkey_in_question
# END of get values-----------------------------------------------------------------------------------
# Update values---------------------------------------------------------------------------------------


@database_common.connection_handler
def edit_comment(id_, message):
    cursor.execute("UPDATE comment SET message = {} WHERE id = {}".format(message, id_))


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
def update_question_by_id(cursor, title, msg, id_):
    cursor.execute("UPDATE question SET title=%s, message=%s WHERE id = {}".format(id_), (title, msg))


@database_common.connection_handler
def update_column(cursor, table, attribute, PK, ID, new_value):
    cursor.execute("UPDATE {} SET {} = '{}' WHERE {} = {} ;".format(table, attribute, str(new_value), PK, ID))
# END of update Values--------------------------------------------------------------------------------
# Add new values--------------------------------------------------------------------------------------


@database_common.connection_handler
def add_question(cursor, list):
    cursor.execute('''INSERT INTO question (submission_time, view_number, vote_number, title, message)
                      VALUES ('{}', {}, {}, '{}', '{}')'''.format(
                                                                    str(dt)[:-7],
                                                                    list[0],
                                                                    list[1],
                                                                    list[2],
                                                                    list[3]
                                                                    ))


@database_common.connection_handler
def add_answer(cursor, list):
    cursor.execute('''INSERT INTO answer (submission_time, vote_number, question_id, message)
                      VALUES ('{}', {}, {}, '{}')'''.format(
                                                            str(dt)[:-7],
                                                            list[0],
                                                            list[1],
                                                            list[2]
                                                            ))


@database_common.connection_handler
def add_comment(cursor, table, id_, comment):
    cursor.execute("INSERT INTO comment ({}, message) VALUES ({} ,'{}')".format(table, id_, comment))
# END of add values-----------------------------------------------------------------------------------
# Delete values --------------------------------------------------------------------------------------


@database_common.connection_handler
def delete_answer_by_id(cursor, ID):
    cursor.execute("DELETE FROM comment where answer_id = {}".format(ID))
    cursor.execute("SELECT question_id FROM answer WHERE id = {}".format(ID))
    question_id = cursor.fetchall()
    cursor.execute("DELETE FROM answer WHERE id = {}".format(ID))
    return question_id[0]["question_id"]


@database_common.connection_handler
def delete_question_and_answer_by_id(cursor, ID):
    cursor.execute("SELECT id FROM answer WHERE question_id = {}".format(ID))
    answerlist = cursor.fetchall()
    for line in answerlist:
        cursor.execute("DELETE FROM comment WHERE answer_id = {}".format(line["id"]))
    cursor.execute("DELETE FROM comment WHERE question_id = {}".format(ID))
    cursor.execute("DELETE FROM answer WHERE question_id = {}".format(ID))
    cursor.execute("DELETE FROM question WHERE id = {}".format(ID))


@database_common.connection_handler
def delete_comment_from_answer(cursor, id_):
    print(id_)
    cursor.execute("DELETE FROM comment WHERE id = {}".format(id_))


@database_common.connection_handler
def delete_comment_from_question(cursor, id_):
    cursor.execute("SELECT id FROM answer WHERE question_id = {}".format(id_))
    answer_id_list = cursor.fetchall()
    print(answer_id_list)
    for line in answer_id_list:
        print(line)
        cursor.execute("DELETE FROM comment WHERE answer_id = {}".format(line["id"]))
    delete_question_and_answer_by_id(id_)


@database_common.connection_handler
def delete_comment(cursor, id_):
    cursor.execute("DELETE FROM comment WHERE id = {}".format(id_))


