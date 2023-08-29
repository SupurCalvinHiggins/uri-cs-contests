from enum import Enum, auto


class Status(Enum):
    SUBMITTED = auto()
    RUNNING = auto()
    PASSED = auto()
    FAILED = auto()
    TIMED_OUT = auto()
