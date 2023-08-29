from flask import Flask, request, render_template, redirect, url_for
from pathlib import Path
from submission import Submission
from program import Program
from contest import Contest
from status import Status
from database import db_insert_or_update, db_iter


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/wordcount", methods=["GET", "POST"])
def wordcount():
    if request.method == "POST":
        file = request.files["file"]
        if Path(file.filename).suffix != '.zip':
            return "Submissions must be ZIP files."
        zip_data = file.read()
        submission = Submission(
            contest=Contest.WORDCOUNT,
            author=request.form["author"],
            email=request.form["email"],
            name=request.form["name"],
            description=request.form["desc"],
            program=Program.from_zip_data(zip_data=zip_data),
            status=Status.SUBMITTED,
        )
        db_insert_or_update(submission)
        return redirect(url_for("wordcount_submission", source_hash="hash"))
    submissions = db_iter()
    return render_template("wordcount.html", submissions=submissions)


@app.route("/wordcount/submission/<string:source_hash>", methods=["GET"])
def wordcount_submission(source_hash: str):
    return render_template("wordcount_submission.html")
