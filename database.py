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
    with con as cur:
        cur.execute(
            """
            CREATE TABLE submissions (
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


def db_insert_or_update(submission: Submission) -> None:
    con = sqlite3.connect(DATABASE_PATH)
    if submission.id is None:
        with con as cur:
            cur.execute(
                """
                INSERT INTO submissions VALUES (
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
                (
                    submission.contest.value,
                    submission.author,
                    submission.email,
                    submission.name,
                    submission.description,
                    submission.status.value,
                    submission.metric,
                    submission.program.language.value,
                    submission.program.zip_data,
                )
            )
    else:
        cur.execute(
            """
            UPDATE submissions SET ()
            """,
            (
                submission.id,
                submission.contest,
                submission.author,
                submission.email,
                submission.name,
                submission.description,
                submission.status,
                submission.metric,
                submission.program.language,
                submission.program.zip_data,
            )
        )

    con.commit()


def db_iter() -> Iterable[Submission]:
    return []


if __name__ == "__main__":
    # db_create()
    submission = Submission(
        id=None,
        contest=Contest.WORDCOUNT,
        author="calvin",
        email="email",
        name="name",
        description="desc",
        program=Program(language=Language.C, zip_data=b""),
        status=Status.SUBMITTED,
        metric=None,
    )
    db_insert_or_update(submission)
