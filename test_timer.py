import time
from timer import Timer


def test_timer() -> None:
    exp_time = 1
    with Timer() as timer:
        time.sleep(exp_time)
    act_time = timer.time / (10 ** 9)
    assert abs(exp_time - act_time) < 0.01
