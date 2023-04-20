from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from search_algorithm_tfidf import recommendations
from search_algorithm_page import userPreferenceJudge, recommendByPages

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/page", methods=["POST"])
def page():
    if request.method == "POST":
        show_select = False
        story = request.form.get("story")
        prefer = userPreferenceJudge(story)
        data = recommendByPages(prefer[0], prefer[1], 9)
        msg = "Based on your prefer, we recommend the following books for you："
        return render_template(
            "index.html", data=data, show_select=show_select, msg=msg
        )


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        book_title = request.form.get("title")
        data = recommendations(book_title)
        if data == False:
            msg = "Could not find the book in the dataset. Do you prefer long story or short story?"
            show_select = True
            return render_template("index.html", msg=msg, show_select=show_select)
        else:
            msg = (
                "Based on the keyword "
                + book_title
                + " you entered, we recommend the following books for you："
            )
            show_select = False
            return render_template(
                "index.html",
                data=recommendations(book_title),
                msg=msg,
                show_select=show_select,
            )
    if request.method == "GET":
        return render_template("index.html")


@app.route("/rating", methods=["POST"])
def submit_rating():
    rating = int(request.form["rating"])
    # Store the rating value in a database or file
    return "Rating submitted successfully!"


if __name__ == "__main__":
    app.run(port=11451)
