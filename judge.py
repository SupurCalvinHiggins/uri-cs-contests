import os
import glob
import time
import subprocess
from database import engine, Contest, Status, SourceType, Submission
from sqlalchemy import select
from sqlalchemy.orm import Session


BUILD_PATH = "build"
SOURCE_PATH = os.path.join(BUILD_PATH, "source")
EXECUTABLE_PATH = os.path.join(BUILD_PATH, "prog")


def setup(source: bytes, source_type: SourceType) -> None:
	"""
	Copy the source file to SOURCE_PATH and compile to EXECUTABLE_PATH. Assumes that the BUILD_PATH has been cleaned.

	Parameters
	----------
	source: The bytes of the source file to compile.
	source_type: The type of the source file to compile.

	Returns
	-------
	None.
	"""

	with open(SOURCE_PATH, "w") as f:
		f.write(source.decode())

	source_type_to_cmd = {
		SourceType.C: f"gcc {SOURCE_PATH} -O3 -std=c17 -o {EXECUTABLE_PATH}",
		SourceType.CPP: f"g++ {SOURCE_PATH} -O3 -std=c++20 -o {EXECUTABLE_PATH}"
	}
	cmd = source_type_to_cmd[source_type]
	subprocess.run(cmd)


def teardown() -> None:
	"""
	Clean BUILD_PATH.

	Returns
	-------
	None.
	"""
	os.makedirs(BUILD_PATH, exist_ok=True)
	for f in glob.glob(os.path.join(BUILD_PATH, "*")):
		os.remove(f)


def time_and_test(args: list[str], expected_stdout: str) -> tuple[Status, int]:
	start_time = time.perf_counter_ns()
	try:
		proc = subprocess.run(
			[f"./{EXECUTABLE_PATH}", *args],
			capture_output=True,
			text=True,
			timeout=5,
		)
	except subprocess.TimeoutExpired:
		return Status.TIMED_OUT, 0
	end_time = time.perf_counter_ns()

	if proc.stdout != expected_stdout:
		return Status.FAILED, end_time - start_time

	return Status.PASSED, end_time - start_time


CONTEST_TO_JUDGE = {
	Contest.WORDCOUNT: judge_wordcount,
}


def collect_submissions() -> list[Submission]:
	with Session(engine) as session:
		stmt = select(Submission).where(Submission.status == Status.SUBMITTED)
		return session.scalars(stmt).all()


COLLECT_DELAY = 10


def main() -> None:
	while True:
		submissions = collect_submissions()
		for submission in submissions:
			teardown()
			setup(submission=submission)
			metric = CONTEST_TO_JUDGE[submission.contest]()
			# TODO: Update submission with metric.


		time.sleep(COLLECT_DELAY)


if __name__ == "__main__":
	main()
