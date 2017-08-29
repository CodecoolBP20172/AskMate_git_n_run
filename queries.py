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
def get_value_of_an_attribute(cursor, table, attribute, PK, ID):
    cursor.execute("SELECT " + attribute + " FROM " + table + " WHERE " + PK + " = " + ID + ";")    
    result = cursor.fetchall()
    value = result[0][attribute]
    return value