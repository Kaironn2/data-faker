from pathlib import Path

from src.erp_bridges.buy_orders_csv import buy_orders_csv
from src.erp_bridges.customers_csv import customers_csv
from src.erp_bridges.ecs_buy_orders_csv import ecs_buy_orders_csv

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

export_path = DATA_DIR / "erp_bridges"

customer_data = customers_csv(str(export_path / "customers.csv"), n=10000)

buy_order_data = buy_orders_csv(
    str(export_path / "buy_orders.csv"), customer_data, n=40000
)

ecs_buy_orders_csv(str(export_path / "ecs_buy_orders.csv"), buy_order_data)
