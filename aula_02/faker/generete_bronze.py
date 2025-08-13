# generate_bronze_data.py
import random
from datetime import datetime, timezone, date
from dateutil.rrule import rrule, DAILY
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

# =========================
# Configurações gerais
# =========================
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("pt_BR")

OUT_DIR = Path("data_bronze")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Período: 2024-01-01 até hoje
START_DATE = date(2024, 1, 1)
END_DATE = datetime.now(timezone.utc).date()

# Clientes / Mercados / Canais
NUM_CLIENTS = 10
MARKETS = ["BR", "US", "EU"]
CHANNELS = ["ONLINE", "DISTRIB", "RETAIL"]

# Ativos (BTC + 3 commodities)  — COFFEE REMOVIDO
ASSETS = [
    ("BTC", "Bitcoin", "coin", "USD"),
    ("GOLD", "Gold", "oz", "USD"),
    ("OIL", "WTI Oil", "bbl", "USD"),
    ("SILVER", "Silver", "oz", "USD"),
]

# =========================
# Helpers
# =========================
def daterange_days(start: date, end: date):
    """Gera apenas dias úteis (segunda a sexta)."""
    for dt in rrule(
        DAILY,
        dtstart=datetime(start.year, start.month, start.day),
        until=datetime(end.year, end.month, end.day),
    ):
        if dt.weekday() < 5:  # 0=segunda, 6=domingo
            yield dt.date()

def pick_btc_qty():
    # 0.01 a 0.50, passo 0.01
    steps = [round(0.01 * i, 2) for i in range(1, 51)]
    return float(random.choice(steps))

def pick_qty(unit: str, asset_code: str) -> float:
    if asset_code == "BTC":
        return pick_btc_qty()
    # 10 a 50 unidades para demais ativos
    return float(random.randint(10, 50))

def pick_tipo_operacao() -> str:
    return random.choice(["COMPRA", "VENDA"])

# =========================
# 1) bronze_customers (simplificada)
# =========================
def build_customers(n=NUM_CLIENTS) -> pd.DataFrame:
    rows = []
    for i in range(1, n + 1):
        rows.append(
            {
                "customer_id": f"C{i:03d}",
                "customer_name": fake.company(),
                "documento": fake.cnpj(),
                "segmento": random.choice(
                    ["Financeiro", "Varejo", "Indústria", "Serviços", "Tecnologia"]
                ),
                "pais": random.choice(["Brasil", "Estados Unidos", "Alemanha"]),
                "estado": fake.estado_sigla(),
                "cidade": fake.city(),
                "created_at": fake.date_time_between(
                    start_date="-3y", end_date="-1y", tzinfo=timezone.utc
                ),
            }
        )
    return pd.DataFrame(rows)

# =========================
# 2) bronze_sales_btc_excel (sem preço; com tipo_operacao)
# =========================
def build_sales_btc_excel(
    customers_df: pd.DataFrame, start: date = START_DATE, end: date = END_DATE
) -> pd.DataFrame:
    rows = []
    tx_id = 1
    for d in daterange_days(start, end):
        total_today = random.randint(30, 40)
        btc_today = int(round(total_today * 0.4))  # ~40% BTC
        for _ in range(btc_today):
            ts = datetime(
                d.year, d.month, d.day, random.randint(9, 20), random.randint(0, 59), tzinfo=timezone.utc
            )
            qty = pick_qty("coin", "BTC")  # decimal
            cliente = customers_df.sample(1).iloc[0]["customer_id"]
            rows.append(
                {
                    "transaction_id": f"BTCX-{tx_id:08d}",
                    "data_hora": ts,
                    "ativo": "BTC",
                    "quantidade": qty,
                    "tipo_operacao": pick_tipo_operacao(),
                    "moeda": "USD",
                    "cliente_id": cliente,
                    "canal": random.choice(CHANNELS),
                    "mercado": random.choice(MARKETS),
                    "arquivo_origem": "btc_planilha.xlsx",
                    "importado_em": datetime.now(timezone.utc),
                }
            )
            tx_id += 1
    df = pd.DataFrame(rows)
    cols = [
        "transaction_id",
        "data_hora",
        "ativo",
        "quantidade",
        "tipo_operacao",
        "moeda",
        "cliente_id",
        "canal",
        "mercado",
        "arquivo_origem",
        "importado_em",
    ]
    return df[cols]

# =========================
# 3) bronze_sales_commodities_sql (simplificada, sem preço; com tipo_operacao)
# =========================
def build_sales_commodities_sql(
    customers_df: pd.DataFrame, start: date = START_DATE, end: date = END_DATE
) -> pd.DataFrame:
    rows = []
    tx_id = 1
    COMMS = [a for a in ASSETS if a[0] != "BTC"]

    for d in daterange_days(start, end):
        total_today = random.randint(30, 40)
        comm_today = total_today - int(round(total_today * 0.4))  # ~60% commodities
        for _ in range(comm_today):
            code, name, unit, currency = random.choice(COMMS)
            ts = datetime(
                d.year, d.month, d.day, random.randint(9, 20), random.randint(0, 59), tzinfo=timezone.utc
            )
            qty = pick_qty(unit, code)
            cliente = customers_df.sample(1).iloc[0]["customer_id"]

            rows.append(
                {
                    "transaction_id": f"COM-{tx_id:08d}",
                    "data_hora": ts,
                    "commodity_code": code,
                    "quantidade": qty,
                    "tipo_operacao": pick_tipo_operacao(),
                    "unidade": unit,
                    "moeda": currency,
                    "cliente_id": cliente,
                    "canal": random.choice(CHANNELS),
                    "mercado": random.choice(MARKETS),
                    "arquivo_origem": "commodities_operacional.sql",
                    "importado_em": datetime.now(timezone.utc),
                }
            )
            tx_id += 1

    df = pd.DataFrame(rows)
    cols = [
        "transaction_id",
        "data_hora",
        "commodity_code",
        "quantidade",
        "tipo_operacao",
        "unidade",
        "moeda",
        "cliente_id",
        "canal",
        "mercado",
        "arquivo_origem",
        "importado_em",
    ]
    return df[cols]

# =========================
# Execução
# =========================
if __name__ == "__main__":
    print(">> Gerando customers...")
    df_customers = build_customers(NUM_CLIENTS)
    df_customers.to_csv(OUT_DIR / "bronze_customers.csv", index=False)

    print(">> Gerando sales_btc_excel (sem preço, com tipo_operacao)...")
    df_sales_btc = build_sales_btc_excel(df_customers)
    df_sales_btc.to_csv(OUT_DIR / "bronze_sales_btc_excel.csv", index=False)

    print(">> Gerando sales_commodities_sql (sem preço, com tipo_operacao)...")
    df_sales_comm = build_sales_commodities_sql(df_customers)
    df_sales_comm.to_csv(OUT_DIR / "bronze_sales_commodities_sql.csv", index=False)

    print("\n=== RESUMO ===")
    print("Customers:", df_customers.shape)
    print("Sales BTC Excel:", df_sales_btc.shape)
    print("Sales Commodities SQL:", df_sales_comm.shape)
    print(f"\nArquivos salvos em: {OUT_DIR.resolve()}")
