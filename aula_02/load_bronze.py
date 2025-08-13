import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis do .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Pasta com os CSVs
DATA_PATH = Path("data_bronze")

def load_csvs_to_db():
    for csv_file in DATA_PATH.glob("*.csv"):
        table_name = csv_file.stem  # Nome sem extensão
        print(f"📥 Lendo {csv_file} para tabela '{table_name}'")

        df = pd.read_csv(csv_file)

        # Insere no banco (append)
        df.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"✅ Inserido {len(df)} registros na tabela '{table_name}'")

if __name__ == "__main__":
    load_csvs_to_db()
