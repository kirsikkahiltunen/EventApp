from app import app
from flask import render_template, request, redirect, session
import events
import users
from datetime import datetime


@app.route("/")
def index():
    events.past_events()
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
            return render_template("index.html", error=True, message="Väärä käyttäjätunnus tai salasana", username=username, password=password)


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

        if len(username) < 3:
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
        csrf_token=request.form["csrf_token"]
        valid_csrf_token = session["csrf_token"]
        if csrf_token == valid_csrf_token:
            event_name = request.form["event_name"]
            event_date_time = request.form["date_time"]
            event_category = request.form.getlist("category")
            event_description = request.form["description"]
            user_id = session["user_id"]
            username = session["username"]
            now = datetime.now()
            formated_now = now.strftime("%Y-%m-%dT%H:%M")
            if event_date_time < formated_now:
                return render_template("create_event.html", error=True, message="Tapahtuman ajankohta ei voi olla menneisyydessä", event_name=event_name, description=event_description)
            events.create_event(user_id, username, event_name,
                                event_date_time, event_category, event_description)

            return redirect("/")


@app.route("/event_info", methods=["GET", "POST"])
def event_info():
    if request.method == "GET":
        return render_template("event_info.html")
    if request.method == "POST":
        csrf_token=request.form["csrf_token"]
        valid_csrf_token = session["csrf_token"]
        if csrf_token == valid_csrf_token:
            event_id = request.form["event_id"]
            user_id = session["user_id"]
            event = events.get_event_by_id(event_id)
            participants = events.get_all_participants(event_id)
            count = len(participants)
            participation_status = events.get_participation(user_id, event_id)
            messages = events.get_messages_by_event(event_id)
            return render_template("event_info.html", messages=messages, participation_status=participation_status, event=event, participants=participants, count=count)


@app.route("/participate_event", methods=["POST"])
def participate_event():
    csrf_token=request.form["csrf_token"]
    valid_csrf_token = session["csrf_token"]
    if csrf_token == valid_csrf_token:
        event_id = request.form["event_id"]
        user_id = session["user_id"]
        username = session["username"]
        already_participate = events.get_participation(user_id, event_id)
        event = events.get_event_by_id(event_id)
        participants = events.get_all_participants(event_id)
        count = len(participants)
        if already_participate:
            print("Käyttäjä, jo ilmoittautunut osallistujaksi")
            participation_status = events.get_participation(user_id, event_id)
            messages = events.get_messages_by_event(event_id)
            return render_template("event_info.html", messages=messages, participation_status=participation_status, event=event, participation=True, message="Olet jo ilmoittautunut tähän tapahtumaan", participants=participants, count=count)
        participate = events.participate_event(user_id, username,  event_id)
        print("Osallistuminen onnistui")
        participation_status = events.get_participation(user_id, event_id)
        messages = events.get_messages_by_event(event_id)
        return render_template("event_info.html", messages=messages, participation_status=participation_status, event=event, message="Ilmoittautuminen tapahtuman osallistujaksi onnistu!", participants=participants, count=count)


@app.route("/send", methods=["POST"])
def send():
    csrf_token=request.form["csrf_token"]
    valid_csrf_token = session["csrf_token"]
    if csrf_token == valid_csrf_token:
        content = request.form["content"]
        event_id = request.form["event_id"]
        title = request.form["title"]
        user_id = session["user_id"]
        username = session["username"]
        event = events.get_event_by_id(event_id)
        events.send_message(user_id, username, event_id, title, content)
        participants = events.get_all_participants(event_id)
        count = len(participants)
        participation_status = events.get_participation(user_id, event_id)
        messages = events.get_messages_by_event(event_id)
        return render_template("event_info.html", messages=messages, participation_status=participation_status, event=event, participants=participants, count=count)


@app.route("/modify_event", methods=["POST"])
def modify_event():
    event_id = request.form["event_id"]
    event = events.get_event_by_id(event_id)
    f_event_date = event.event_date_time.strftime('%Y-%m-%dT%H:%M')
    return render_template("modify.html", event=event, event_date=f_event_date)


@app.route("/modify_event_info", methods=["POST"])
def modify_event_info():
    csrf_token=request.form["csrf_token"]
    valid_csrf_token = session["csrf_token"]
    if csrf_token == valid_csrf_token:
        event_id = request.form["event_id"]
        user_id = session["user_id"]
        event_name = request.form["event_name"]
        event_date_time = request.form["date_time"]
        event_description = request.form["description"]
        events.update_event_info(
            event_id, user_id, event_name, event_date_time, event_description)
        event = events.get_event_by_id(event_id)
        participants = events.get_all_participants(event_id)
        count = len(participants)
        participation_status = events.get_participation(user_id, event_id)
        messages = events.get_messages_by_event(event_id)
        return render_template("event_info.html", messages=messages, participation_status=participation_status,  event=event, modified=True, message="Muutosten tallentaminen onnistui", participants=participants, count=count)


@app.route("/delete_event", methods=["POST"])
def delete_event():
    csrf_token=request.form["csrf_token"]
    valid_csrf_token = session["csrf_token"]
    if csrf_token == valid_csrf_token:
        event_id = request.form["event_id"]
        user_id = session["user_id"]
        events.delete_event(event_id, user_id)
        events_list = events.get_all()
        count = len(events_list)
        return render_template("index.html", events=events_list, count=count, deleted=True, message="Tapahtuman poistaminen onnistui")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    search_results = events.find(query)
    count = len(search_results)
    return render_template("index.html", events=search_results, count=count)


@app.route("/delete_participation", methods=["POST"])
def delete_participation():
    csrf_token=request.form["csrf_token"]
    valid_csrf_token = session["csrf_token"]
    if csrf_token == valid_csrf_token:
        event_id = request.form["event_id"]
        user_id = session["user_id"]
        events.delete_participation(event_id, user_id)
        event = events.get_event_by_id(event_id)
        participants = events.get_all_participants(event_id)
        count = len(participants)
        participation_status = events.get_participation(user_id, event_id)
        messages = events.get_messages_by_event(event_id)
        return render_template("event_info.html", messages=messages, participation_status=participation_status, event=event, count=count, deleted=True, message="Tapahtumaan ilmoittautuminen peruttu", participants=participants)


@app.route("/respond", methods=["POST"])
def respond():
    event_id = request.form["event_id"]
    user_id = request.form["user_id"]
    username = request.form["username"]
    return render_template("respond_message.html", event_id=event_id, user_id=user_id, username=username)


@app.route("/send_respond", methods=["POST"])
def send_respond():
    csrf_token=request.form["csrf_token"]
    valid_csrf_token = session["csrf_token"]
    if csrf_token == valid_csrf_token:
        content = request.form["content"]
        event_id = request.form["event_id"]
        title = request.form["title"]
        user_id = request.form["user_id"]
        username = request.form["username"]
        event = events.get_event_by_id(event_id)
        events.send_message(user_id, username, event_id, title, content)
        participants = events.get_all_participants(event_id)
        count = len(participants)
        participation_status = events.get_participation(user_id, event_id)
        messages = events.get_messages_by_event(event_id)
        return render_template("event_info.html", messages=messages, participation_status=participation_status, event=event, participants=participants, count=count)


@app.route("/my_messages", methods=["GET"])
def my_messages():
    user_id = session["user_id"]
    messages = events.get_messages_by_user_id(user_id)
    return render_template("sent_messages.html", messages=messages)
