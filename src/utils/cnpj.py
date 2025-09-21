import re
from faker import Faker

FAKER = Faker("pt_BR")


def random_cnpjs(n: int = 5, only_digits: bool = False) -> list[str]:
    cnpjs = [FAKER.cnpj() for _ in range(n)]
    if only_digits:
        cnpjs = [re.sub(r"\D", "", c) for c in cnpjs]
    return cnpjs
