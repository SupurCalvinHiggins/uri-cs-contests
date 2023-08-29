from enum import Enum


class Status(Enum):
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
