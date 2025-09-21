import csv
import random
from datetime import datetime
from faker import Faker
from typing import TypedDict

from src.erp_bridges.customers_csv import CustomerData
from src.utils.date import random_datetime
from src.utils.phone import brazil_phone


class BuyOrderData(TypedDict):
    order_number: str
    buy_order_date: datetime
    status: str


def buy_orders_csv(
    file: str, customer_data: list[CustomerData], n: int = 20
) -> list[BuyOrderData]:
    fake = Faker("pt_BR")
    email_to_cpf = {}
    cpf_to_email = {}

    buy_order_data: list[BuyOrderData] = []

    end = datetime(2025, 12, 31, 23, 59, 59)

    statuses = ["Pendente", "Enviado", "Entregue", "Cancelado"]
    payment_types = ["Pix", "Cartão de Crédito", "Boleto Bancário"]

    with open(file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(
            [
                "Pedido #",
                "ID do Pedido",
                "Firstname",
                "Lastname",
                "Email",
                "Grupo do Cliente",
                "Número CPF/CNPJ",
                "Comprado Em",
                "Shipping Telephone",
                "Status",
                "Número do Rastreador",
                "Qtd. Vendida",
                "Frete",
                "Desconto",
                "Payment Type",
                "Total da Venda",
            ]
        )

        order_number = 100000000
        order_id = 227000

        for _ in range(n):
            customer = random.choice(customer_data)
            email = customer["email"]
            customer_since = customer["customer_since"]

            if email in email_to_cpf:
                cpf = email_to_cpf[email]
            else:
                while True:
                    cpf = fake.cpf()
                    if cpf not in cpf_to_email:
                        break
                email_to_cpf[email] = cpf
                cpf_to_email[cpf] = email

            name = fake.name().split()
            firstname = name[0]
            lastname = " ".join(name[1:]) if len(name) > 1 else ""

            customer_group = random.choice(["Comum", "vip", "Influencer"])
            buy_order_date = random_datetime(customer_since, end)
            phone = brazil_phone()
            status = random.choice(statuses)
            tracking_number = fake.swift() if status == "Enviado" else ""
            quantity = random.randint(1, 5)
            shipping_amount = f"R${random.uniform(0, 30):.2f}".replace(".", ",")
            discount = (
                f"R${random.uniform(0, 20):.2f}".replace(".", ",")
                if random.random() > 0.7
                else "R$0,00"
            )
            payment_type = random.choice(payment_types)
            total_amount = f"R${random.uniform(50, 500):.2f}".replace(".", ",")

            order_number += 1
            order_id += 1

            writer.writerow(
                [
                    order_number,
                    order_id,
                    firstname,
                    lastname,
                    email,
                    customer_group,
                    cpf,
                    buy_order_date.strftime("%d/%m/%Y %H:%M:%S"),
                    phone,
                    status,
                    tracking_number,
                    quantity,
                    shipping_amount,
                    discount,
                    payment_type,
                    total_amount,
                ]
            )

            buy_order_data.append(
                {
                    "order_number": str(order_number),
                    "buy_order_date": buy_order_date,
                    "status": status,
                }
            )

    return buy_order_data
