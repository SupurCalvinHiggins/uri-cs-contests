import os
import glob
import time
import subprocess
from typing import Optional
from database import engine, Contest, Status, SourceType, Submission
from sqlalchemy import select
from sqlalchemy.orm import Session


BUILD_PATH = "build"
SOURCE_PATH = os.path.join(BUILD_PATH, "source")
EXECUTABLE_PATH = os.path.join(BUILD_PATH, "prog")


def setup(submission: Submission) -> None:
	teardown()

	with open(SOURCE_PATH, "w") as f:
		f.write(submission.source)

	if submission.source_type == SourceType.C:
		subprocess.run(f"gcc {SOURCE_PATH} -O3 -std=c17 -o {EXECUTABLE_PATH}")
	elif submission.source_type == SourceType.CPP:
		subprocess.run(f"g++ {SOURCE_PATH} -O3 -std=c++20 -o {EXECUTABLE_PATH}")


def teardown() -> None:
	os.makedirs(BUILD_PATH, exist_ok=True)
	for f in glob.glob(os.path.join(BUILD_PATH, "*")):
		os.remove(f)


def judge_wordcount() -> Optional[int]:
	start_time = time.perf_counter_ns()
	try:
		subprocess.run(
			f"./{EXECUTABLE_PATH} data/wordcount/large.txt",
			capture_output=True,
			timeout=5,
		)
	except subprocess.TimeoutExpired:
		return None
	end_time = time.perf_counter_ns()
	return end_time - start_time


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
			setup(submission=submission)
			metric = CONTEST_TO_JUDGE[submission.contest]()
			teardown()
			# TODO: Update submission with metric.


		time.sleep(COLLECT_DELAY)


if __name__ == "__main__":
	main()
