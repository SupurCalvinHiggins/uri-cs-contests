from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


DATABASE_URL = "sqlite:///submissions.db"
engine = create_engine(DATABASE_URL)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        submission = Submission(
            contest=Contest.WORDCOUNT,
            author="Calvin Higgins",
            email="",
            name="test",
            desc="test",
            source="int main() { return 0; }".encode(),
            source_type=SourceType.C,
            source_hash="abc",
            status=Status.SUBMITTED,
            metric=None,
        )
        session.add_all([submission])
        session.commit()

    from sqlalchemy import select
    with Session(engine) as session:
        stmt = select(Submission).where(Submission.status == Status.SUBMITTED)
        print(session.scalars(stmt).all())