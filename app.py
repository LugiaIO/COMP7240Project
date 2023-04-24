from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    session,
    url_for,
    send_file,
)
from flask_cors import CORS
from hybrid_algorithm import recommendations, feedback
from search_algorithm_page import userPreferenceJudge, recommendByPages
from portal import register, login, getUserId
import os

# instantiate the app
app = Flask(__name__)


class Config(object):
    SECRET_KEY = "17727141091ceb1b7b9ef7ae59513ca8"


app.config.from_object(Config())
# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/dldb")
def downloadFile():
    path = "./model/database.db"
    return send_file(path, as_attachment=True)


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("username", None)
    # Redirect to login page
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def loginPortal():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        if login(username, password):
            session["loggedin"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            msg = "Invalid username or password!"
            return render_template("login.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def registerPortal():
    msg = ""
    if request.method == "GET":
        return render_template("register.html", msg=msg)
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        if register(username, password) == False:
            msg = "This username already exists!"
            return render_template("register.html", msg=msg)
        msg = "You have successfully registered! Please Login!"
        return redirect(url_for("loginPortal"))


@app.route("/page", methods=["POST"])
def page():
    if request.method == "POST":
        show_select = False
        username = session.get("username")
        loggedin = session.get("loggedin")
        story = request.form.get("story")
        prefer = userPreferenceJudge(story)
        (data, hidden_score) = recommendByPages(prefer[0], prefer[1], 6)
        msg = "Based on your prefer, we recommend the following books for you："
        return render_template(
            "index.html",
            data=data,
            show_select=show_select,
            msg=msg,
            username=username,
            loggedin=loggedin,
            hidden_score=hidden_score,
        )


@app.route("/")
def home():
    return redirect(url_for("index"))


@app.route("/index", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if "loggedin" in session:
            book_title = request.form.get("title")
            username = session.get("username")
            loggedin = session.get("loggedin")
            user_id = getUserId(username)
            data = recommendations(user_id, book_title)
            if data == False:
                msg = "Could not find the book in the dataset. Do you prefer long story or short story?"
                show_select = True
                return render_template(
                    "index.html",
                    msg=msg,
                    show_select=show_select,
                    username=username,
                    loggedin=loggedin,
                )
            else:
                msg = (
                    "Based on the title "
                    + book_title
                    + " you entered, we recommend the following books for you："
                )
                show_select = False
                return render_template(
                    "index.html",
                    data=data,
                    msg=msg,
                    show_select=show_select,
                    username=username,
                    loggedin=loggedin,
                )
        else:
            show_select = False
            msg = "You have not registered, please register first!"
            return render_template("index.html", msg=msg, show_select=show_select)
    if request.method == "GET":
        username = session.get("username")
        loggedin = session.get("loggedin")
        return render_template("index.html", username=username, loggedin=loggedin)


@app.route("/rating", methods=["POST"])
def submitRating():
    rating = int(request.form["rating"])
    booktitle = request.form["booktitle"]
    username = session.get("username")
    loggedin = session.get("loggedin")
    data = feedback(username, booktitle, rating, num_recommendations=6)
    show_select = False
    msg = (
        "Based on your rating for "
        + booktitle
        + ", we recommend the following books for you："
    )
    return render_template(
        "index.html",
        data=data,
        show_select=show_select,
        msg=msg,
        username=username,
        loggedin=loggedin,
    )


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8081)), host="0.0.0.0", debug=True)
