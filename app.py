from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)
app.config["SECRET_KEY"] = "NlfXwuU9XjHD0CrtXDqSxLLyQgunDXXv6JfLWHmotenCqrwT9SVE0sWqFB8Ppdu5"  
# app.config["MONGO_URI"] = "mongodb+srv://cgsoledispa:soledispa1@cluster0.l8edvdn.mongodb.net/cluster0"
app.config["MONGO_URI"] = "mongodb+srv://heroe:heroe@cluster0.wkxtx.mongodb.net/chris"

mongo = PyMongo(app)

@app.route("/")
def index():
    if "username" in session:
        return f"Hello, {session['username']}!"
    return "Welcome to the authentication example!"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password").encode("utf-8")

        hashed_password = hashpw(password, gensalt())

        user = {
            "username": username,
            "password": hashed_password
        }

        mongo.db.users.insert_one(user)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password").encode("utf-8")

        user = mongo.db.users.find_one({"username": username})

        if user and checkpw(password, user["password"]):
            session["username"] = username
            return redirect(url_for("index"))

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)