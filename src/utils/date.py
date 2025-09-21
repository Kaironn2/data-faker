import random
from datetime import datetime


def random_datetime(start: datetime, end: datetime) -> datetime:
    return start + (end - start) * random.random()
