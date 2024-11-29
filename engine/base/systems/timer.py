from time import time
from typing import Callable
from collections import deque

from engine.core import System


class Timer:
    repeat: bool
    duration: float
    function: Callable

    _next_update: float

    def __init__(self, repeat: bool, duration: float, function: Callable) -> None:
        self.repeat = repeat
        self.duration = duration
        self.function = function

        self._next_update = time() + duration

    def update(self) -> bool:
        if time() >= self._next_update:
            self._next_update = time() + self.duration

            self.function()
            
            return self.repeat
        return True


class TimerSystem(System):
    _timers: dict[int, Timer]
    _next_timer_id: int
    _finished_timers: deque[int]

    def __init__(self) -> None:
        self._timers = {}
        self._next_timer_id = 0
        self._finished_timers = deque()

    def add_timer(self, repeat: bool, duration: float, function: Callable) -> int:
        timer_id = self._next_timer_id
        self._next_timer_id += 1 

        self._timers[timer_id] = Timer(repeat, duration, function)

    def finish_timer(self, timer_id: int) -> None:
        self._finished_timers.append(timer_id)

    def update(self, delta: float) -> None:
        finished_timers = set(self._finished_timers)

        self._timers = {
            timer_id: timer
            for timer_id, timer in self._timers.items()
            if timer_id not in finished_timers and timer.update()
        }
