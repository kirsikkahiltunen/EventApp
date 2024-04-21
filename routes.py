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
            return render_template("index.html", error=True, message = "Väärä käyttäjätunnus tai salasana", username=username, password=password)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(username)<3:
            return render_template("register.html", error=True, message="Käyttäjätunnuksen tulee olla yli kolmen merkin mittainen", username=username, password1=password1, password2=password2)
        
        if " " in username:
            return render_template("register.html", error=True, message="Käyttäjätunnus ei voi sisältää välilyöntejä", username=username, password1=password1, password2=password2)

        if password1 == password2:
            if users.valid_password(password1):
                if users.register(username, password1):
                    return redirect("/")
                else:
                    return render_template("register.html", error=True, message="Salasanan tulee olla yli 8 merkkiä pitkä ja sisältää ainakin yhden pienenkirjaimen, isonkirjaimen, numeron ja erikoismerkin", username=username, password1=password1, password2=password2)
            
            else:
                return render_template("register.html", error=True, message="Salasanan tulee olla yli 8 merkkiä pitkä ja sisältää ainakin yhden pienenkirjaimen, isonkirjaimen, numeron ja erikoismerkin", username=username, password1=password1, password2=password2)
        
        else:
            return render_template("register.html", error=True, message="Salasanat eivät täsmää", username=username, password1=password1, password2=password2)
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

        