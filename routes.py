from app import app
from flask import render_template, request, redirect
import events
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("invalidlogin.html", message = "Väärä käyttäjätunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 == password2:
            if users.register(username, password1):
                return redirect("/")
            
            else:
                return render_template("register.html", username=username)
        
        else:
            return render_template("register.html", username=username)
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

        