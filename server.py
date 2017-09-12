from flask import Flask, render_template, redirect, request, session
import datetime
from datetime import timezone
from operator import itemgetter
import queries
app = Flask(__name__)

# session----------------------------------------------------------


@app.route('/login', methods=['POST'])
def log_in():
    usernames_and_passwords = queries.get_usernames_and_passwords()
    try:
        if usernames_and_passwords[request.form['username']] == request.form['password']:
            session['logged_in'] = True
            session.username = request.form['username']
            error = False
    except KeyError:
        pass
    return route_list()


@app.route('/logout')
def log_out():
    session['logged_in'] = False
    return route_list()


# END session------------------------------------------------------

# Index------------------------------------------------------------


@app.route("/all")
def route_list_all():
    questions = queries.get_questions_for_index()
    return render_template("list.html", questions=questions)


@app.route("/")
def route_list():
    questions = queries.get_latest_five_questions()
    return render_template("list.html", questions=questions)


@app.route("/getsearch", methods=['POST'])
def route_get_search():
    questions = queries.get_search_results(request.form["searchbox"])
    return render_template("list.html", questions=questions)


@app.route("/<aspect>=<desc>")
def route_list_aspect(aspect, desc):
    questions = queries.get_questions_for_index_ordered(aspect, desc)
    return render_template("list.html", questions=questions)

# index-END--------------------------------------------------------
# Question---------------------------------------------------------


@app.route("/question/<int:id_>", methods=['GET'])
def route_question(id_):
    question = queries.get_question_by_id(id_)
    answers = queries.get_answers_by_question_id(id_)
    question_comments = queries.get_question_comments_by_question_id(id_,"question_id")
    answer_comments = queries.get_all_answer_comments()
    return render_template(
        "question.html", 
        question=question, 
        answers=answers, 
        questioncomments=question_comments,
        answercomments=answer_comments,
        id_=str(id_))


@app.route("/question/<int:id_>/save", methods=['POST'])
def route_question_save(id_):
    queries.update_question_by_id(request.form["title"], request.form["question"], id_)
    return redirect("/question/" + str(id_))


@app.route("/question/<int:ID>/delete", methods=["GET"])
def route_question_delete(ID):
    queries.delete_comment_from_question(ID)
    return redirect("/")


@app.route("/question/<int:id_>/edit", methods=['GET'])
def route_question_edit(id_):
    question = queries.get_question_by_id(id_)
    return render_template(
        "form.html",
        page_title="Edit a question",
        action_link="/question/"+str(id_)+"/save",
        title_of_question=question[0]["title"],
        question=question[0]["message"])

# Question END-----------------------------------------------------------------
# Answer ----------------------------------------------------------------------


@app.route("/answer/<int:ID>/edit/save", methods=["POST"])
def route_answer_edit_save(ID):
    edited_text = request.form["answer_edit_text"]
    queries.update_column("answer", "message", "id", str(ID), edited_text)
    question_id = queries.get_value_of_an_attribute("answer", "question_id", "id", str(ID))
    return redirect("/question/"+str(question_id))


@app.route("/answer/<int:ID>/edit", methods=["GET"])
def route_answer_edit(ID):
    message_to_edit = queries.get_value_of_an_attribute("answer", "message", "id", str(ID))
    question_id = queries.get_value_of_an_attribute("answer", "question_id", "id", str(ID))
    question = queries.get_question_by_id(question_id)
    answers = queries.get_answers_by_question_id(question_id)
    question_comments = queries.get_question_comments_by_question_id(question_id, "question_id")
    answer_comments = queries.get_question_comments_by_question_id(question_id, "answer_id")
    return render_template(
        "question.html", 
        id_to_edit=ID, 
        question=question, 
        answers=answers, 
        questioncomments=question_comments, 
        answercomments=answer_comments, 
        id_=str(question_id))


@app.route("/answer/<int:ID>/delete", methods=["GET"])
def route_answer_delete(ID):
    QID = queries.delete_answer_by_id(ID)
    return redirect("/question/"+str(QID))

    
@app.route("/give-answer/<int:ID>", methods=["POST"])
def route_add_answer(ID):
    list_to_write = [0, ID, request.form["answer_text"]]
    queries.add_answer(list_to_write)
    return redirect("/question/"+str(ID))

# Answer END------------------------------------------------------------------------
# Comment----------------------------------------------------------------


@app.route("/give_comment/<table>/<int:id_>", methods=['POST'])
def route_give_comment(table, id_):
    comment_to_write = request.form["comment"]
    queries.add_comment(table, id_, comment_to_write)
    if table == "question_id":
        return redirect("/question/" + str(id_))
    elif table == "answer_id":
        q_id = queries.get_question_id_from_answer_id(id_)
        return redirect("/question/" + str(q_id))


@app.route("/<int:question_id>/delete_comment_from_answer/<int:id_>")
def route_delete_comment(question_id, id_):
    queries.delete_comment_from_answer(id_)
    return redirect("/question/"+str(question_id))


@app.route("/<int:question_id>/delete_comment/<int:id_>")
def route_deleteasd_comment(question_id, id_):
    queries.delete_comment(id_)
    return redirect("/question/"+str(question_id))


@app.route("/<int:question_id>/edit_comment/<int:id_>")
def route_edit_comment(question_id, id_):
    queries.edit_comment(comment, message, id_, request.form["edited_comment"])
    return redirect("/question/"+str(question_id))
# Comment END------------------------------------------------------------


@app.route("/add-question", methods=["POST"])
def route_add():
    list_to_write = [0, 0, request.form["title"], request.form["question"]]
    queries.add_question(list_to_write)
    return redirect("/")


@app.route("/question/<int:ID>/vote-up", methods=['GET'])
def route_question_vote_up(ID):
    queries.modify_value_of_data("question", "vote_number", "id", str(ID), 1)
    return redirect("/question/"+str(ID))


@app.route("/question/<int:ID>/vote-down", methods=['GET'])
def route_question_vote_down(ID):
    queries.modify_value_of_data("question", "vote_number", "id", str(ID), -1)
    return redirect("/question/"+str(ID))


@app.route("/answer/<int:ID>/vote-up", methods=['GET'])
def route_answer_vote_up(ID):
    queries.modify_value_of_data("answer", "vote_number", "id", str(ID), 1)
    question_id = queries.get_value_of_an_attribute("answer", "question_id", "id", str(ID))
    return redirect("/question/"+str(question_id))


@app.route("/answer/<int:ID>/vote-down", methods=['GET'])
def route_answer_vote_down(ID):
    queries.modify_value_of_data("answer", "vote_number", "id", str(ID), -1)
    question_id = queries.get_value_of_an_attribute("answer", "question_id", "id", str(ID))
    return redirect("/question/"+str(question_id))
    

@app.route("/question+1view/<int:ID>", methods=["GET"])
def route_question_view(ID):
    queries.modify_value_of_data("question", "view_number", "id", str(ID), 1)
    return redirect("/question/"+str(ID))


@app.route("/ask-question")
def route_ask():
    return render_template("form.html", page_title="Ask a question", action_link="/add-question")


if __name__ == "__main__":
    app.secret_key = "app_magic"  # Change the content of this string
    app.run(
        debug=True,
        port=5000
    )
