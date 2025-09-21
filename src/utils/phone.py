import random


def brazil_phone() -> str:
    ddd = random.randint(11, 99)
    if random.random() > 0.5:
        number = random.randint(100000000, 999999999)
    else:
        number = random.randint(10000000, 99999999)
    return f"({ddd}) {number}"
