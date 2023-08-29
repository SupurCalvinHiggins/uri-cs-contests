from __future__ import annotations


import time
from typing import Optional


class Timer:
    def __init__(self):
        self._start_time: Optional[int] = None
        self._end_time: Optional[int] = None

    def __enter__(self) -> Timer:
        self.__init__()
        self._start_time = time.perf_counter_ns()
        return self

    def __exit__(self, *exc) -> None:
        self._end_time = time.perf_counter_ns()

    @property
    def time(self) -> int:
        assert self._start_time is not None
        assert self._end_time is not None
        return self._end_time - self._start_time
