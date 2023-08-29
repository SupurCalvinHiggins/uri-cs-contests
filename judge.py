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

	with open(f"{SOURCE_PATH}.cpp", "w") as f:
		f.write(source.decode())

	source_type_to_cmd = {
		SourceType.C: f"gcc {SOURCE_PATH}.c -O3 -std=c17 -o {EXECUTABLE_PATH}",
		SourceType.CPP: f"g++ {SOURCE_PATH}.cpp -O3 -std=c++20 -o {EXECUTABLE_PATH}"
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
	except Exception:
		return Status.FAILED, 0
	end_time = time.perf_counter_ns()

	if proc.stdout.strip() != expected_stdout:
		return Status.FAILED, end_time - start_time

	return Status.PASSED, end_time - start_time


def collect_submissions() -> list[Submission]:
	with Session(engine) as session:
		stmt = select(Submission).where(Submission.status == Status.SUBMITTED)
		return session.scalars(stmt).all()


COLLECT_DELAY = 10
CONTEST_TO_TESTCASES = {
	Contest.WORDCOUNT: [
		{
			"args": ["data/wordcount/tiny.txt"],
			"expected_stdout": "11",
		},
	]
}


def main() -> None:
	while True:
		submissions = collect_submissions()
		for submission in submissions:
			teardown()
			setup(source=submission.source, source_type=submission.source_type)
			total_metric = 0
			status = Status.PASSED
			for kwargs in CONTEST_TO_TESTCASES[submission.contest]:
				status, metric = time_and_test(**kwargs)
				total_metric += metric
				if status != status.PASSED:
					break
			submission.status = status
			submission.metric = total_metric
			with Session(engine) as session:
				session.add(submission)
				session.commit()

		time.sleep(COLLECT_DELAY)


if __name__ == "__main__":
	main()
