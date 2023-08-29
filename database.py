from typing import Iterable

from contest import Contest
from program import Program
from status import Status
from language import Language
from submission import Submission
import sqlite3


DATABASE_PATH = "app.db"


def db_create() -> None:
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE submissions (
            id INTEGER PRIMARY KEY,
            contest TEXT NOT NULL, 
            author TEXT NOT NULL, 
            email TEXT NOT NULL, 
            name TEXT NOT NULL, 
            description TEXT NOT NULL, 
            status TEXT NOT NULL, 
            metric INTEGER, 
            language TEXT NOT NULL, 
            zip_data BLOB NOT NULL
        )
        """
    )
    con.commit()
    con.close()


def db_insert_or_update(submission: Submission) -> None:
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    if submission.id is None:
        cur.execute(
            """
            INSERT INTO submissions 
            (contest, author, email, name, description, status, metric, language, zip_data) 
            VALUES (
                :contest,
                :author,
                :email,
                :name,
                :description,
                :status,
                :metric,
                :language,
                :zip_data
            )
            """,
            db_adapt_submission(submission)
        )
    else:
        cur.execute(
            """
            UPDATE submissions 
            SET 
                contest = :contest,
                author = :author,
                email = :email,
                name = :name,
                description = :description,
                status = :status,
                metric = :metric,
                language = :language,
                zip_data = :zip_data 
            WHERE 
                id = :id
            """,
            db_adapt_submission(submission)
        )
    con.commit()
    con.close()


def db_iter() -> Iterable[Submission]:
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM submissions")
    rows = cur.fetchall()
    con.close()
    return [db_convert_submission(row) for row in rows]


def db_adapt_submission(submission: Submission) -> dict:
    return {
        "id": submission.id,
        "contest": submission.contest.value,
        "author": submission.author,
        "email": submission.email,
        "name": submission.name,
        "description": submission.description,
        "status": submission.status.value,
        "metric": submission.metric,
        "language": submission.program.language.value,
        "zip_data": submission.program.zip_data,
    }


def db_convert_submission(row: tuple) -> Submission:
    return Submission(
        id=row[0],
        contest=Contest(row[1]),
        author=row[2],
        email=row[3],
        name=row[4],
        description=row[5],
        status=Status(row[6]),
        metric=row[7],
        program=Program(language=Language(row[8]), zip_data=row[9]),
    )


if __name__ == "__main__":
    db_create()
    # submission = Submission(
    #     id=None,
    #     contest=Contest.WORDCOUNT,
    #     author="calvin",
    #     email="email",
    #     name="name",
    #     description="desc",
    #     program=Program(language=Language.C, zip_data=b""),
    #     status=Status.SUBMITTED,
    #     metric=None,
    # )
    # db_insert_or_update(submission)
    # db_insert_or_update(submission)
    # submission.id = 1
    # submission.name = "new name"
    # db_insert_or_update(submission)
    # print(db_iter())
