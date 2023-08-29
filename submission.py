from __future__ import annotations


from dataclasses import dataclass
from typing import Optional
from contest import Contest
from program import Program
from status import Status


@dataclass
class Submission:
    id: Optional[int]
    contest: Contest
    author: str
    email: str
    name: str
    description: str
    program: Program
    status: Status
    metric: Optional[int]
