import csv
import random
from datetime import datetime
from typing import TypedDict

from faker import Faker

from src.utils.date import random_datetime
from src.utils.phone import brazil_phone


class CustomerData(TypedDict):
    email: str
    customer_since: datetime


def customers_csv(file: str, n: int = 10) -> list[CustomerData]:
    fake = Faker("pt_BR")
    data: list[CustomerData] = []

    start = datetime(2020, 1, 1, 0, 0, 0)
    end = datetime(2025, 12, 31, 23, 59, 59)

    with open(file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(
            [
                "Créditos / Vale Presentes",
                "ID",
                "Nome",
                "E-mail",
                "Grupo",
                "Telefone",
                "CEP",
                "País",
                "Estado",
                "Cliente Desde",
            ]
        )

        for i in range(n):
            name = fake.name()
            email = fake.unique.email()
            customer_group = random.choice(["Comum", "vip"])
            phone = brazil_phone() if random.random() > 0.3 else ""
            zip_code = fake.postcode() if random.random() > 0.3 else ""
            country = "Brasil" if random.random() > 0.5 else ""
            state = fake.estado_sigla() if random.random() > 0.3 else ""
            customer_since = random_datetime(start, end)

            currency = "R$0,00"

            customer_id = 571900 + (n - i)

            writer.writerow(
                [
                    currency,
                    customer_id,
                    name,
                    email,
                    customer_group,
                    phone,
                    zip_code,
                    country,
                    state,
                    customer_since.strftime("%d/%m/%Y %H:%M:%S"),
                ]
            )

            data.append({"email": email, "customer_since": customer_since})

    return data
