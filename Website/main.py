from flask import Flask, render_template, redirect, request, session
import mysql.connector
import gunicorn

app = Flask(__name__)
app.secret_key = "coolguy"

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wagner2020",
    database="seconddb"
)


mycursor = my_db.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

@app.route("/")
def home():
    if "username" in session:
        list = ''
        return render_template("index.html", user=session("username"), list=list)
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        sql = "SELECT username FROM users WHERE username = %s AND password = %s"
        values = [username, password]
        mycursor.execute(sql, values)

        myresult = mycursor.fetchall()

        if len(myresult) > 0:
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", message="Wrong username or password.")

    else:
        return render_template("login.html")
        mycursor.execute(sql, value)

        myresult = mycursor.fetchall()


@app.route("/register", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if (password != confirm_password):
            return render_template("register.html", message="passwords don't match")

        sql = "SELECT username FROM users WHERE username = %s AND password = %s"
        value = (username, password)
        mycursor.execute(sql, value)

        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            return render_template("register.html", message="Username already taken. Try something new!")
        else:
            sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
            values = [username, password]
            mycursor.execute(sql, values)
            my_db.commit()

            session["username"] = username
            return redirect("/")
    else:
        return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop("username", None)
    return render_template("login.html")


if __name__ == '__main__':
    import os

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)