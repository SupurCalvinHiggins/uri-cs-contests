from __future__ import annotations

import time
import subprocess
from pathlib import Path
from timer import Timer


def setup(build_path: Path, program: Program) -> None:
    build_path.mkdir(exist_ok=True)
    if build_path.exists():
        for path in build_path.iterdir():
            path.unlink()
    program.compile(build_path=build_path)


def execute_cmd(cmd: str, timed: bool) -> tuple[str, int]:
    with Timer() as timer:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    return proc.stdout.strip(), (timer.time if timed else 0)


CONTEST_TO_TESTCASES = {
    Contest.WORDCOUNT: [
        {
            "cmd": "./prog data/wordcount/tiny.txt",
            "exp": "11",
            "timed": False,
        },
        {
            "cmd": "./prog data/wordcount/large.txt",
            "exp": "906912",
            "timed": True,
        }
    ]
}


def main() -> None:
    while True:
        for submission in submissions:
            setup(build_path=BUILD_PATH, program=submission.program)

            metric = 0
            status = Status.PASSED
            for testcase in CONTEST_TO_TESTCASES[submission.contest]:
                try:
                    act, partial_metric = execute_cmd(cmd=testcase["cmd"], timed=testcase["timed"])
                    metric += partial_metric
                except subprocess.TimeoutExpired:
                    status = Status.TIMED_OUT
                except:
                    status = Status.FAILED

                if act != testcase["exp"]:
                    status = Status.FAILED

                if status != Status.PASSED:
                    break

            submission.status = status
            submission.metric = total_metric
            with Session(engine) as session:
                session.add(submission)
                session.commit()
        time.sleep(COLLECT_DELAY)

