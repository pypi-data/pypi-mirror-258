from dataclasses import dataclass
from typing import Union


def plural(n: Union[int, float], name: str) -> str:
    return name + ("s" if abs(n) >= 2 else "")


@dataclass
class TimeDecomposition:
    days: int
    hours: int
    minutes: int
    seconds: int
    microseconds: float

    def __init__(
        self,
        days: float = 0.0,
        hours: float = 0.0,
        minutes: float = 0.0,
        seconds: float = 0.0,
        microseconds: float = 0.0,
    ):
        self.days = int(days)
        hours += (days - self.days) * 24
        self.hours = int(hours)
        minutes += (hours - self.hours) * 60
        self.minutes = int(minutes)
        seconds += (minutes - self.minutes) * 60
        self.seconds = int(seconds)
        microseconds += (seconds - self.seconds) * 1e6
        seconds, self.microseconds = divmod(microseconds, 1000000)
        self.seconds += int(seconds)
        minutes, self.seconds = divmod(self.seconds, 60)
        self.minutes += int(minutes)
        hours, self.minutes = divmod(self.minutes, 60)
        self.hours += int(hours)
        days, self.hours = divmod(self.hours, 24)
        self.days += int(days)

    def total_seconds(self) -> float:
        return (
            self.days * 86400
            + self.hours * 3600
            + self.minutes * 60
            + self.seconds
            + self.microseconds * 1e-6
        )

    def pretty(self) -> str:
        raw = f"{self.total_seconds():g} s"
        vals = [
            (num, f"{num:g} {plural(num, name)}")
            for num, name in zip(
                [
                    self.days,
                    self.hours,
                    self.minutes,
                    self.seconds,
                    self.microseconds,
                    0,
                ],
                ["day", "hour", "minute", "second", "microsecond", ""],
            )
        ]
        for (num, main), (snum, sub) in zip(vals[:-1], vals[1:]):
            if num > 0:
                return raw + (f" ({main} {sub})" if snum > 0 else f" ({main})")
        return raw


def pretty_time(seconds: float) -> str:
    """Formats a duration in human-readable units

    The output format is `<raw duration> s (<number> <unit1> [<number2> <unit2>])
    """
    return TimeDecomposition(seconds=seconds).pretty()


def pretty_bytes(bytes: int, decimal: bool = False) -> str:
    """Format a number of bytes in human-readable units

    The output format is `<raw number> B (<human-readable number> <unit>)`

    Parameters
    ----------
    bytes: int
        Value to format
    decimal: bool
        If True, use decimal units (e.g. MB) instead of binary (e.g. MiB)

    Returns
    -------
    str
        Formatted number
    """
    factor = 1000 if decimal else 1024
    unit = "B" if decimal else "iB"
    raw = f"{bytes} {plural(bytes, 'byte')}"
    if bytes < factor:
        return raw
    scaled = bytes
    prefixes = ["k", "M", "G", "T", "P", "E"]
    for i, prefix in enumerate(prefixes):
        scaled /= factor
        if scaled < factor or i == len(prefixes) - 1:
            return raw + f" ({scaled:g} {prefix}{unit})"
    assert False
