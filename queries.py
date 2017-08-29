import database_common


@database_common.connection_handler
def get_mentor_names(cursor):
    cursor.execute("SELECT CONCAT(first_name, ' ', last_name) as full_name FROM mentors ORDER BY first_name")
    names = cursor.fetchall()
    return names
