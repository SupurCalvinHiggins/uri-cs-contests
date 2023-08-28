import io
import hashlib
import os.path

from models import *
from database import engine
from flask import Flask, request, render_template, redirect, url_for
from flask.globals import app_ctx
from sqlalchemy.orm import scoped_session, sessionmaker


UPLOAD_FOLDER = "submissions"


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# This next section of code is non-obvious. When handling a request, we need to ensure that any database
# connections we use are scoped to the request. In general, we cannot assume that each request runs on an individual
# thread. Therefore, we need to extract an ID for the request. Flask does not automatically generate IDs for requests,
# so instead we take the ID of the current request object. This is stored in an internal Flask data structure that was
# found by examining the source of Flask-SQLAlchemy which implements the same hack.
app.session = scoped_session(
    session_factory=sessionmaker(engine),
    scopefunc=lambda: id(app_ctx._get_current_object())
)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/wordcount", methods=["GET", "POST"])
def wordcount():
    if request.method == "POST":
        author = request.form["author"]
        email = request.form["email"]
        name = request.form["name"]
        desc = request.form["desc"]
        file = request.files["file"]
        source = file.read()
        source_type = SourceType.from_str(os.path.splitext(file.filename)[-1][1:].upper())
        if source_type is None:
            return f"Invalid source type {os.path.splitext(file.filename)[-1]}."
        source_hash = hashlib.sha256(source).hexdigest()
        submission = Submission(
            contest=Contest.WORDCOUNT,
            author=author,
            email=email,
            name=name,
            desc=desc,
            source=source,
            source_type=source_type,
            source_hash=source_hash,
            status=Status.SUBMITTED,
            metric=None,
        )
        app.session.add(submission)
        app.session.commit()
        return redirect(url_for("wordcount_submission", source_hash=source_hash))
    submissions = app.session.query(Submission).all()
    return render_template("wordcount.html", submissions=submissions)


@app.route("/wordcount/submission/<string:source_hash>", methods=["GET"])
def wordcount_submission(source_hash: str):
    return render_template("wordcount_submission.html")
