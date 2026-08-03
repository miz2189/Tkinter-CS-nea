import sqlite3
import bcrypt
import random
from datetime import timedelta
from datetime import datetime, date

connection = sqlite3.connect("quiz.db")
cursor = connection.cursor()


def login(username, password, attempts):
    if attempts == 3:
        return "Lock"  # password attempt limit hit
    else:
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result == None:
            return None  # no username exists
        elif bcrypt.checkpw(password.encode("utf-8"), result[0]) == True:
            cursor.execute(
                "SELECT role,name FROM users WHERE username = ?", (username,)
            )
            output = cursor.fetchall()
            details = [[row[0], row[1]] for row in output]
            return details  # password is correct
        else:
            return False  # password is wrong


def register(name, age, username, password, role):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    try:
        output = cursor.execute(
            "INSERT INTO users(name,age,username,password,role) Values(?,?,?,?,?)",
            (name, age, username, hash, role),
        )
    except sqlite3.IntegrityError:
        return False
    # making a leaderboard record so it can be updated by update_score
    connection.commit()
    if role == "student":
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO leaderboard(user_id,score) Values(?,?)", (user_id, 0)
        )
        connection.commit()
    return True


def num_quiz():
    # selecting all titles and their creator's user id from quizzes table
    cursor.execute("SELECT title, user_id FROM quizzes")
    output = cursor.fetchall()
    # reformatting the output into a 2d array
    quizzes = [[row[0], row[1]] for row in output]
    for row in quizzes:
        # username is being extracted by using the user id
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (row[1],))
        output = cursor.fetchone()[0]
        row[1] = output
    title = []
    for row in quizzes:
        # quiz title and username are being combined to be displayed properly
        title.append(row[0] + " by " + row[1])
    return title


def access_questions(quiz_title):
    # the title is being seperated from the username
    quiz = quiz_title.split("by")
    # fetching user_id based on username
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (quiz[1].strip(),))
    user_id = cursor.fetchone()[0]
    # fetching all details about question depending on quiz_title
    cursor.execute(
        "SELECT question_text, question_id, question_type FROM questions WHERE quiz_id IN (SELECT quiz_id FROM quizzes WHERE title = ? AND user_id = ?)",
        (quiz[0].strip(), user_id),
    )
    output = cursor.fetchall()
    # output is reformatted in 2d array
    question = [[row[0], row[1], row[2]] for row in output]
    return question


def access_answers(question_id):
    # fetching anwer details from answers
    cursor.execute(
        "SELECT answer_text, is_correct FROM answers WHERE question_id = ?",
        (question_id,),
    )
    output = cursor.fetchall()
    # output being put in a 2d array
    answer = [[row[0], row[1]] for row in output]
    return answer


def save_score(quiz_title, score, username):
    current_day = date.today()
    # extracting quiz title
    quiz = quiz_title.split("by")
    # featching quiz creator user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (quiz[1].strip(),))
    creator_id = cursor.fetchone()[0]
    # extracting quiz title fetching quiz id
    cursor.execute(
        "SELECT quiz_id FROM quizzes WHERE title = ? AND user_id = ?",
        (quiz[0].strip(), creator_id),
    )
    quiz_id = cursor.fetchone()
    # fetching user id of the user attempting
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    # using all details to insert a record
    cursor.execute(
        "INSERT INTO results(quiz_id,user_id,result,date_completed) Values(?,?,?,?)",
        (quiz_id[0], user_id, score, current_day),
    )
    connection.commit()


def create_quiz(quiz_name, by):
    # fetching user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (by,))
    user_id = cursor.fetchone()[0]
    # creating record of quiz
    cursor.execute(
        "INSERT INTO quizzes(title,user_id) Values(?,?)", (quiz_name, user_id)
    )
    connection.commit()


def save_question(quiz_name, by, type, text):
    # fetching user id
    cursor.execute("SELECT user_id FROM users WHERE username = (?)", (by,))
    user_id = cursor.fetchone()[0]
    # fetching quiz id
    cursor.execute(
        "SELECT quiz_id FROM quizzes WHERE title = ? AND user_id = ?",
        (quiz_name, user_id),
    )
    id = cursor.fetchone()
    # creating record of question
    cursor.execute(
        "INSERT INTO questions(question_text,question_type,quiz_id) Values(?,?,?)",
        (text, type, id[0]),
    )
    connection.commit()
    return cursor.lastrowid


def save_answer(question_id, answer_text, is_correct):
    cursor.execute(
        "INSERT INTO answers(question_id,answer_text,is_correct) Values(?,?,?)",
        (question_id, answer_text, is_correct),
    )
    connection.commit()


# generating code
def code_generate():
    # loop to to keep generate code until unique code is generated
    while True:
        code = ""
        # creating code
        for _ in range(5):
            code = code + str(random.randint(1, 9))
        # checking if the unique code already exists
        cursor.execute("SELECT 1 FROM assignment WHERE code = ?", (code,))
        exists = cursor.fetchone()
        if not exists:
            return code


def assignment(quiz_title, due_time, username):
    # fetching user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    quiz = quiz_title.split("by")
    # fetching creator id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (quiz[1].strip(),))
    creator_id = cursor.fetchone()[0]
    # fetching quiz id
    cursor.execute(
        "SELECT quiz_id FROM quizzes WHERE title = ? AND user_id = ?",
        (quiz[0].strip(), creator_id),
    )
    quiz_id = cursor.fetchone()[0]
    # getting the date
    current_day = date.today()
    end_date = current_day + timedelta(days=due_time)
    # generating code
    code = code_generate()
    cursor.execute(
        "INSERT INTO assignment(quiz_id,user_id,code,assigned_on,expires_on) Values(?,?,?,?,?)",
        (quiz_id, user_id, code, current_day, end_date),
    )
    connection.commit()
    return code


def quiz_fetcher(code):
    cursor.execute("SELECT quiz_id,expires_on From assignment WHERE code = ?", (code,))
    output = cursor.fetchall()
    if not output:
        # code has no quiz associated with
        return None
    values = [[row[0], row[1]] for row in output]
    current_day = date.today()
    # converting string into datetime value
    expires_date = datetime.strptime(values[0][1], "%Y-%m-%d").date()
    # checking if assignment is past due date
    if expires_date > current_day:
        # fetching quiz title and user id
        cursor.execute(
            "SELECT title,user_id From quizzes WHERE quiz_id = ?", (values[0][0],)
        )
        output = cursor.fetchall()
        # fetching username
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (output[0][1],))
        username = cursor.fetchone()
        # combining quiz title and username
        title = output[0][0] + " by " + username[0]
        return title
    else:
        # assigment is expired
        return 0


# will not create new entrys for new users as it will be created in register


def update_score(username):
    # fetching user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    # fetching all results of user
    cursor.execute("SELECT result FROM results WHERE user_id = ? ", (user_id,))
    output = cursor.fetchall()
    # putting data into a list
    scores = [row[0] for row in output]
    # leaderboard is updated usinng sum of array
    cursor.execute(
        "UPDATE leaderboard SET score = ? WHERE user_id = ? ", (sum(scores), user_id)
    )
    connection.commit()


def get_score(username):
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT score FROM leaderboard WHERE user_id = ?", (user_id,))
    output = cursor.fetchone()[0]
    return output


def leaderboard():
    # fetching all records from leaderboard ordered by descending order
    cursor.execute("SELECT user_id, score FROM leaderboard ORDER BY score DESC")
    output = cursor.fetchall()
    # formatting the output into a 2d list
    scores = [[row[0], row[1]] for row in output]
    # converting each user id into username for each record
    for row in scores:
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (row[0],))
        output = cursor.fetchone()[0]
        row[0] = output
    return scores


def student_reports(username):
    # fetching user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    # fetching quiz details
    cursor.execute(
        "SELECT quiz_id,result,date_completed FROM results WHERE user_id = ?",
        (user_id,),
    )
    output = cursor.fetchall()
    # turnning from tuple to 2d list
    list = [[str(row[0]), row[1], row[2]] for row in output]
    quiz_attempted = []
    # changing data in list
    for row in list:
        # fetching quiz title and creator id
        cursor.execute(
            "SELECT title, user_id FROM quizzes WHERE quiz_id = ?", (row[0],)
        )
        output = cursor.fetchall()
        # fetching creator username
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (output[0][1],))
        username = cursor.fetchone()[0]
        row.append(username)
        # replacing user id with quiz id
        row[0] = output[0][0]
        # adding elements in quiz that tracks quiz attempted by user
        if quiz_attempted.count(output[0][0].strip() + " by " + username) == 0:
            quiz_attempted.append(output[0][0] + " by " + username)
    return list, quiz_attempted


def teacher_quizzes(username):
    # fetching user id of the teacher
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]

    # fetching the quiz id and the title quiz created by the teacher
    cursor.execute("SELECT quiz_id, title FROM quizzes WHERE user_id = ?", (user_id,))
    # putting data into 2D list
    quiz_ids = [[row[0], row[1]] for row in cursor.fetchall()]
    quizzes = []
    students = []
    # constructing quiz title that will displayed to teacher
    for i in range(len(quiz_ids)):
        quizzes.append(quiz_ids[i][1] + " by " + username)
        # fetching details of each student attempt for each quiz created by teacher
        cursor.execute(
            "SELECT user_id, quiz_id, result, date_completed FROM results WHERE quiz_id = ?",
            (quiz_ids[i][0],),
        )
        output = cursor.fetchall()
        students.extend([list(row) for row in output])

    # replacing data from fetched quiz attempt details
    for i in range(len(students)):
        cursor.execute(
            "SELECT username FROM users WHERE user_id = ?", (students[i][0],)
        )
        students[i][0] = cursor.fetchone()[0]
        cursor.execute("SELECT title FROM quizzes WHERE quiz_id = ?", (students[i][1],))
        students[i][1] = cursor.fetchone()[0]
    return quizzes, students


def tquiz_list(username):
    # fetching teacher user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    id = cursor.fetchone()[0]
    # fetching titles of all quizzes teacher has created
    cursor.execute("SELECT title FROM quizzes WHERE user_id = ?", (id,))
    output = [row[0] for row in cursor.fetchall()]
    # returning quizzes
    return output


def quiz_details(title, username):
    # fetching teacher user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    id = cursor.fetchone()[0]

    # fetching quiz id
    cursor.execute(
        "SELECT quiz_id FROM quizzes WHERE title = ? AND user_id = ?", (title, id)
    )
    quiz_id = cursor.fetchone()[0]

    # fetching all question types
    cursor.execute("SELECT question_type FROM questions WHERE quiz_id = ?", (quiz_id,))
    type = cursor.fetchall()
    # counting questiontype to see how many questions the quiz has
    details = [len(type), type[0][0]]

    return details


def delete_quiz_data(username, title):
    # fetching teacher user id
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    id = cursor.fetchone()[0]

    # fetching quiz id
    cursor.execute(
        "SELECT quiz_id FROM quizzes WHERE title = ? AND user_id = ?", (title, id)
    )
    quiz_id = cursor.fetchone()[0]

    # fetching question id to acess questions
    cursor.execute("SELECT question_id FROM questions WHERE quiz_id = ?", (quiz_id,))
    question_id = [row[0] for row in cursor.fetchall()]

    # deleting question
    cursor.execute("DELETE FROM questions WHERE quiz_id = ?", (quiz_id,))
    # deleting all answer for each question
    for i in question_id:
        cursor.execute("DELETE FROM answers WHERE question_id = ?", (i,))

    connection.commit()


light_blue = "#0078D7"
grey = "#808080"
black = "#000000"
white = "#FFFFFF"
red = "#FF0000"
charcoal_grey = "#36454F"
