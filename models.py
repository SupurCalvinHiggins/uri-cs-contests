from __future__ import annotations
from typing import Optional
from enum import Enum, auto
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base


class Status(Enum):
    SUBMITTED = auto()
    RUNNING = auto()
    PASSED = auto()
    FAILED = auto()


class Contest(Enum):
    WORDCOUNT = auto()


class SourceType(Enum):
    C = auto()
    CPP = auto()

    @staticmethod
    def from_str(s: str) -> Optional[SourceType]:
        try:
            return SourceType[s]
        except KeyError:
            return None


Base = declarative_base()


class Submission(Base):
    __tablename__: str = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    contest: Mapped[Contest]
    author: Mapped[str]
    email: Mapped[str]
    name: Mapped[str]
    desc: Mapped[str]
    source: Mapped[bytes] = mapped_column(LargeBinary())
    source_type: Mapped[SourceType]
    source_hash: Mapped[str]
    status: Mapped[Status]
    metric: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return (
            "Submission("
            f"id={self.id}, "
            f"contest={self.contest}, "
            f"author={self.author}, "
            f"email={self.email}, "
            f"name={self.name}, "
            f"desc={self.desc}, "
            f"source={self.source}, "
            f"source_type={self.source_type}, "
            f"source_hash={self.source_hash}, "
            f"status={self.status}, "
            f"metric={self.metric}, "
            ")"
        )