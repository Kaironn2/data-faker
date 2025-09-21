import csv
import random
from datetime import timedelta
from faker import Faker

from src.erp_bridges.buy_orders_csv import BuyOrderData
from src.utils.cnpj import random_cnpjs

COLUMNS = [
    "Numero da Ordem",
    "Número do Pedido",
    "ID",
    "Observação Interna",
    "Data do Pagamento",
    "Nome do contato",
    "CEP do contato",
    "Cidade do contato",
    "UF do Contato",
    "Data de Entrega",
    "Transportadora",
    "Forma Frete",
    "Forma de pagamento",
]

CARRIERS = [
    "retirada centro",
    "retirada leste",
    "retirada oeste",
    "azul",
    "j&t",
    "correios",
    "entrega local",
]

CARRIER_TYPES = ["SEDEX", "PAC"]

PAYMENTS = ["pagarme5_cc", "pagarme5_pix", "pagarme5_boleto", "free"]

FAKER = Faker("pt_BR")


def ecs_buy_orders_csv(file: str, orders: list[BuyOrderData]):
    cnpjs = random_cnpjs(5, only_digits=True)
    coupons = ["CUPOM10", "CUPOM20", "DESCONTO5", "PROMO15", ""]
    payment_types = ["Pix", "Cartão de Crédito", "Boleto Bancário", "Cartão Loja"]

    with open(file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=COLUMNS,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()

        ecs_order_id = 300000

        for order in orders:
            ecs_order_id += 1
            order_number = order["order_number"]
            status = order["status"]
            buy_order_date = order["buy_order_date"]

            payment_date_dt = buy_order_date + timedelta(days=random.randint(0, 4))
            payment_date = payment_date_dt.strftime("%d/%m/%Y")

            ecs_delivery_date = ""
            if status.lower() == "entregue":
                ecs_delivery_dt = buy_order_date + timedelta(days=random.randint(1, 10))
                ecs_delivery_date = ecs_delivery_dt.strftime("%d/%m/%Y %H:%M:%S")

            carrier = random.choice(CARRIERS)
            carrier_type = ""
            if carrier == "correios":
                carrier_type = random.choice(CARRIER_TYPES)

            cnpj = random.choice(cnpjs)
            payment_method = random.choice(PAYMENTS)
            coupon = random.choice(coupons)
            coupon_text = f" {coupon}" if coupon else ""
            prazo = random.randint(1, 20)
            details = (
                f"Forma de pagamento: {payment_method}_cnpj_{cnpj}\n"
                f"Serviços de Entrega - Entrega Normal - Em média {prazo} dia(s) úteis\n"
                f"Meio de pagamento: {payment_method}{coupon_text}"
            )

            row = {
                "Numero da Ordem": order_number,
                "Número do Pedido": order_number,
                "ID": ecs_order_id,
                "Observação Interna": details,
                "Data do Pagamento": payment_date,
                "Nome do contato": FAKER.name(),
                "CEP do contato": FAKER.postcode(),
                "Cidade do contato": FAKER.city(),
                "UF do Contato": FAKER.estado_sigla(),
                "Data de Entrega": ecs_delivery_date,
                "Transportadora": carrier,
                "Forma Frete": carrier_type,
                "Forma de pagamento": random.choice(payment_types),
            }

            writer.writerow(row)

    return True
