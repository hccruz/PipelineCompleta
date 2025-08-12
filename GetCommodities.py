# GetCommodities.py
import yfinance as yf
import pandas as pd
from datetime import datetime

def get_commodities_df() -> pd.DataFrame:
    symbols = ["GC=F", "CL=F", "SI=F"]  # Ouro, Petróleo, Prata
    dfs = []

    for sym in symbols:
        # Última cotação (1 minuto)
        ultimo_df = yf.Ticker(sym).history(period="1d", interval="1m")[["Close"]].tail(1)

        # Renomear e adicionar colunas extras
        ultimo_df = ultimo_df.rename(columns={"Close": "preco"})
        ultimo_df["ativo"] = sym
        ultimo_df["moeda"] = "USD"
        ultimo_df["horario_coleta"] = datetime.now()

        # Garantir ordem das colunas
        ultimo_df = ultimo_df[["ativo", "preco", "moeda", "horario_coleta"]]

        dfs.append(ultimo_df)

    # Concatenar todos em um único DataFrame
    return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    df = get_commodities_df()
    print(df)
    print("✅ Cotações das commodities obtidas com sucesso!")
