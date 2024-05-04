from app import app
from flask import render_template, request, redirect, session
import events
import users

@app.route("/")
def index():
    events_list = events.get_all()
    count = len(events_list)
    return render_template("index.html", events=events_list, count=count)

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
        already_user = users.username_already_exists(username)

        if already_user:
            return render_template("register.html", error=True, message="Käyttäjätunnus on jo käytössä", username=username, password1=password1, password2=password2)

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

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    
    if request.method == "GET":
        return render_template("create_event.html")
    if request.method == "POST":
        event_name = request.form["event_name"]
        event_date_time = request.form["date_time"]
        event_category = request.form.getlist("category")
        event_description = request.form["description"]
        user_id = session["user_id"]
        username = session["username"]

        events.create_event(user_id, username, event_name, event_date_time, event_category, event_description)

        return redirect("/")
    

@app.route("/event_info", methods=["GET", "POST"])
def event_info():
    if request.method == "GET":
        return render_template("event_info.html")
    if request.method == "POST":
        event_id = request.form["event_id"]
        event = events.get_event_by_id(event_id)
        return render_template("event_info.html", event=event)

@app.route("/participate_event", methods=["POST"])
def participate_event():
    event_id = request.form["event_id"]
    user_id = session["user_id"]
    username = session["username"]
    already_participate=events.get_participation(user_id, event_id)
    event = events.get_event_by_id(event_id)
    if already_participate:
        print("Käyttäjä, jo ilmoittautunut osallistujaksi")
        return render_template("event_info.html", event=event)
    print("Osallistuminen onnistui")
    return render_template("event_info.html", event=event)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    event_id = request.form["event_id"]
    user_id = session["user_id"]
    event = events.get_event_by_id(event_id)
    events.send_message(user_id, event_id, content)
    return render_template("event_info.html", event=event)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    search_results=events.find(query)
    count=len(search_results)
    return render_template("index.html", events=search_results, count=count)